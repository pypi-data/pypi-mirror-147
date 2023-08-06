# MIT License
#
# Copyright (c) 2022 Noah McIlraith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import io
from unittest import TestCase
from functools import partial


class LuckypostTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leaf_storage = {}
        self.branch_storage = {}

    def store_block(
            self,
            block_type: str,
            block_hash: bytes,
            block_data: bytes) -> None:
        """Used for testing trees."""
        if block_type == 'leaf':
            self.leaf_storage[block_hash] = block_data
        elif block_type == 'branch':
            self.branch_storage[block_hash] = block_data
        else:
            raise ValueError("unsupported block type: %s" % block_type)

    def fetch_block(
            self,
            block_type: str,
            block_hash: bytes) -> bytes:
        """Used for testing trees."""
        if block_type == 'leaf':
            return self.leaf_storage[block_hash]
        elif block_type == 'branch':
            return self.branch_storage[block_hash]
        else:
            raise ValueError("unsupported block type: %s" % block_type)

    def test_varint(self):
        from luckypost import encode_varint, decode_varint
        self.assertRaises(ValueError, partial(encode_varint, -1))
        self.assertRaises(EOFError, partial(decode_varint, io.BytesIO(b'')))
        # truncated
        self.assertRaises(
            EOFError,
            partial(decode_varint, io.BytesIO(encode_varint(128)[0:1])))

    def test_lb32(self):
        from luckypost import lb32decode, lb32encode
        a = b'testing'
        b = lb32encode(a)
        c = lb32decode(b)
        self.assertEqual(a, c)
    
    def test_get_hash_func_code(self):
        from luckypost import create_blockhash, get_hash_func_code
        hash_func_code = 56
        vh = create_blockhash(hash_func_code, 32, b'')
        self.assertEqual(get_hash_func_code(vh), hash_func_code)

    def test_block_split(self):
        from luckypost import (
            join_blockhash,
            split_blockhash,
            get_hash_func_code,
            get_block_size,
            InvalidHashError)
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        digest_bytes = b'\00' * digest_size
        blockhash_bytes = join_blockhash(
            hash_func_code, block_size, digest_bytes)
        self.assertEqual(
            (hash_func_code, block_size, digest_bytes),
            split_blockhash(blockhash_bytes))
        # try reading individual components of the blockhash
        self.assertEqual(
            get_hash_func_code(blockhash_bytes),
            hash_func_code)
        self.assertEqual(
            get_block_size(blockhash_bytes),
            block_size)
        # try corrupt blockhash
        self.assertRaises(
            InvalidHashError,
            partial(split_blockhash, blockhash_bytes[:2]))

    def test_block_hash_creation(self):
        from luckypost import create_blockhash, UnsupportedHashFunctionError
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        a = create_blockhash(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            block_size=block_size,
            block_data=b"testing")
        b = create_blockhash(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            block_size=block_size,
            block_data=io.BytesIO(b"testing"))
        self.assertEqual(a, b)
        self.assertRaises(
            UnsupportedHashFunctionError,
            partial(create_blockhash,
                    hash_func_code=0,  # 0 is unused, will cause error
                    digest_size=digest_size,
                    block_size=block_size,
                    block_data=b"testing"))
        self.assertRaises(
            ValueError,
            partial(create_blockhash,
                    hash_func_code=False,  # must be an int
                    digest_size=digest_size,
                    block_size=block_size,
                    block_data=b"testing"))
        # blake
        create_blockhash(
            hash_func_code=112,
            digest_size=digest_size,
            block_size=block_size,
            block_data=b"testing")
        create_blockhash(
            hash_func_code=126,
            digest_size=digest_size,
            block_size=block_size,
            block_data=io.BytesIO(b"testing"))
        # auto block size
        create_blockhash(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            block_data=io.BytesIO(b"testing"))
        # auto block size (non-buffer)
        create_blockhash(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            block_data=b'testing')
        # function input
        def test():
            return b'testing message returned from func here'
        create_blockhash(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            block_data=test)

    def test_test(self):
        self.assertRaises(
            ValueError, partial(self.store_block, 'somethingelse', b'', b''))
        self.assertRaises(
            ValueError, partial(self.fetch_block, 'somethingelse', b''))

    def _test_tree(self, hash_func_code, digest_size, block_size, f):
        from luckypost import create_blocktree, split_treehash
        content_size, treehash = create_blocktree(
            hash_func_code=hash_func_code,
            digest_size=digest_size,
            block_size=block_size,
            byte_stream=f,
            content_size=len(f.getvalue()),
            store_block_func=self.store_block)
        hash_func_code2, block_size2, root_hash_bytes = \
            split_treehash(treehash)
        self.assertEqual(hash_func_code2, hash_func_code)
        self.assertEqual(content_size, len(f.getvalue()))
        self.assertEqual(block_size2, block_size)
        self.assertEqual(len(root_hash_bytes), digest_size)
        return content_size, treehash

    def test_tree(self):
        from io import BytesIO
        from luckypost import read_blocktree
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        # create trees from each message
        messages = [
            b'',
            b'short message',
            b'long message' * 100,
            b'very very long message' * 10000,
        ]
        content_sizes_and_treehashes = []
        for message in messages:
            content_size_and_treehash = self._test_tree(
                hash_func_code, digest_size, block_size, BytesIO(message))
            content_sizes_and_treehashes.append(content_size_and_treehash)
        for content_size, treehash in content_sizes_and_treehashes:
            b''.join(read_blocktree(content_size, treehash, self.fetch_block))

    def test_tree_range(self):
        import secrets
        from io import BytesIO
        from luckypost import read_blocktree_range
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        data = secrets.token_bytes(1024 * 1024)
        limit = 10
        offset = 1
        content_size, treehash = self._test_tree(
            hash_func_code, digest_size, block_size, BytesIO(data))
        result = b''.join(read_blocktree_range(
            content_size, treehash, self.fetch_block, offset, limit))
        comparison = data[offset:offset + limit]
        self.assertEqual(result, comparison)

    def test_leaf_count(self):
        from luckypost import get_leaf_count
        self.assertEqual(get_leaf_count(64, 256), 1)
        self.assertEqual(get_leaf_count(256, 256), 1)
        self.assertEqual(get_leaf_count(256 + 1, 256), 2)
        self.assertEqual(get_leaf_count(1024, 256), 4)

    def test_treeio(self):
        from luckypost import create_blocktree, BlockTreeIO
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        data = b"testing " * 100
        content_size, treehash_bytes = create_blocktree(
            hash_func_code,
            digest_size,
            block_size,
            byte_stream=io.BytesIO(data),
            content_size=len(data),
            store_block_func=self.store_block)
        treeio = BlockTreeIO(content_size, treehash_bytes, self.fetch_block)
        # validate position returned by `tell()`
        self.assertEqual(treeio.tell(), 0)
        # read first 5 bytes
        read_bytes = treeio.read(5)
        # validate bytes
        self.assertEqual(read_bytes, data[:5])
        # validate position returned by `tell()`
        self.assertEqual(treeio.tell(), 5)
        # seek back to zero and check again
        treeio.seek(0)
        self.assertEqual(treeio.tell(), 0)
        # seek to end and try to read one byte past the end
        treeio.seek(0, 2)
        self.assertEqual(treeio.tell(), len(data))
        self.assertEqual(treeio.read(1), b'')
        # seek to a middle-ish position
        treeio.seek(100)
        self.assertEqual(treeio.tell(), 100)
        self.assertEqual(treeio.read(10), data[100:110])
        treeio.seek(-200, 2)
        self.assertEqual(treeio.tell(), len(data) - 200)
        self.assertEqual(treeio.read(5), data[-200:-195])
        treeio.seek(-400, 2)
        self.assertEqual(treeio.tell(), len(data) - 400)
        self.assertEqual(treeio.read(5), data[-400:-395])
        # read last 5 bytes
        treeio.seek(-5, 2)
        self.assertEqual(treeio.tell(), len(data) - 5)
        self.assertEqual(treeio.read(5), data[-5:])
        # ValueError when seeking positive number relative to end
        self.assertRaises(ValueError, partial(treeio.seek, 1, 2))
        # ValueError when invalid value for 'whence' argument
        self.assertRaises(ValueError, partial(treeio.seek, 0, 3))
        # relative seek
        treeio.seek(0)
        treeio.seek(5, 1)
        self.assertEqual(treeio.tell(), 5)
        treeio.seek(0, 1)  # go nowhere
        self.assertEqual(treeio.tell(), 5)
        self.assertEqual(treeio.read(5), data[5:10])
        treeio.seek(-10, 1)  # go back to start
        self.assertEqual(treeio.tell(), 0)
        # invalid read amount number
        self.assertRaises(ValueError, partial(treeio.read, 'abc'))

    def test_child_count(self):
        from luckypost import get_child_count_per_branch
        # no branches in a tree without leaves
        a = list(get_child_count_per_branch(0, 2))
        self.assertEqual(a, [])
        # no branches in a tree with one leaf
        b = list(get_child_count_per_branch(1, 2))
        self.assertEqual(b, [])

    def test_tree2(self):
        from luckypost import create_blocktree, BlockTreeIO
        import secrets
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        data = secrets.token_bytes(512)
        content_size, treehash_bytes = create_blocktree(
            hash_func_code,
            digest_size,
            block_size,
            byte_stream=io.BytesIO(data),
            content_size=len(data),
            store_block_func=self.store_block)
        treeio = BlockTreeIO(content_size, treehash_bytes, self.fetch_block)
        output = treeio.read()
        self.assertEqual(output, data)

    def test_tree3(self):
        from luckypost import create_blocktree, read_blocktree
        hash_func_code = 56
        digest_size = 32
        block_size = 256
        data = b"testing" * 1024
        content_size, treehash_bytes = create_blocktree(
            hash_func_code,
            digest_size,
            block_size,
            byte_stream=io.BytesIO(data),
            content_size=len(data),
            store_block_func=self.store_block
        )
        output = b''.join(
            read_blocktree(content_size, treehash_bytes, self.fetch_block))
        self.assertEqual(output, data)

    def test_specific_block_size(self):
        from luckypost import get_specific_block_size
        a = get_specific_block_size(
            digest_size=32,
            content_size=512,
            block_size=256,
            tree_level=1,
            position=1)
        self.assertEqual(a, 256)
        # one block tree
        a = get_specific_block_size(
            digest_size=32,
            content_size=256,
            block_size=256,
            tree_level=0,
            position=0)
        self.assertEqual(a, 256)
        # zero block tree
        func = partial(
            get_specific_block_size,
            digest_size=32,
            content_size=0,
            block_size=256,
            tree_level=0,
            position=0)
        self.assertRaises(ValueError, func)  # no blocks to get size of
        # three block tree
        a = get_specific_block_size(
            digest_size=32,
            content_size=512,
            block_size=256,
            tree_level=0,
            position=0)
        self.assertEqual(a, 64)

    def test_specific_block_size2(self):
        from luckypost import get_specific_block_size
        a = get_specific_block_size(
            digest_size=32,
            content_size=2432750,
            block_size=1048576,
            tree_level=1,
            position=2)
        self.assertNotEqual(2, a)
