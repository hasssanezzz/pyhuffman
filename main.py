from heapq import heapify, heappop, heappush
from os.path import getsize

class Node:
  def __init__(self, chr: str, freq: int, left: 'Node' = None, right: 'Node' = None):
    self.chr = chr
    self.freq = freq
    self.left = left
    self.right = right
  
  def __lt__(self, other: 'Node'):
    return self.freq < other.freq

class TextualHuffman:
  
  def generate_tree(text: str) -> Node:
    if not text:
      return
    
    freq = {}
    for i in text:
      if i in freq:
        freq[i] += 1
      else:
        freq[i] = 1
    
    nodes_pq = [Node(k, v) for k, v in freq.items()]
    heapify(nodes_pq)
    
    while len(nodes_pq) > 1:
      left, right = heappop(nodes_pq), heappop(nodes_pq)
      newfreq = left.freq + right.freq
      heappush(nodes_pq, Node(None, newfreq, left, right))
    
    return nodes_pq[0]

  def generate_encoding_map(text: str, tree: Node) -> dict:
    mp = {}
    
    def dfs(node: Node, counter: str):
      if node.left:
        dfs(node.left, counter + '0')
      if node.right:
        dfs(node.right, counter + '1')
        
      if node.chr:
        mp[node.chr] = counter
        
    dfs(tree, '')
    return mp

  def write_encoded_data(text: str, map: dict, outfilepath: str):
    r = ''
    
    for c in text:
      r += map[c]

    open(outfilepath, 'wb').write(
      bytes(int(r, 2).to_bytes((len(r) + 7) // 8, 'big')))
  
  def encode_and_write(text: str, outfilepath: str):
    tree = TextualHuffman.generate_tree(text)
    map = TextualHuffman.generate_encoding_map(text, tree)
    TextualHuffman.write_encoded_data(text, map, outfilepath)

  def decode_bits(compressed_bits: str, tree: Node):
    result = ""
    node = tree
    for c in compressed_bits:
      if c == '0':
        node = node.left
      else:
        node = node.right
      
      if node.chr:
        result += node.chr
        node = tree
    return result

  def encode_file(infilepath: str, outfilepath: str):
    text = open(infilepath, 'r', encoding='utf8').read()
    TextualHuffman.encode_and_write(text, outfilepath)
    
    return outfilepath
  
  def decode_file(tree: Node, infilepath: str, outfilepath: str):
    binary_data = open(infilepath, 'rb').open()
    bits = bin(int.from_bytes(binary_data, 'big'))[2:]
    open(outfilepath, 'wb').write(TextualHuffman.decode_bits(bits, tree))


# TODO sync cli arguments
infile = 'random.txt'
outfile = 'compressed.bin'

TextualHuffman.encode_file(infile, outfile)

print('Original file size:', getsize(infile), 'bytes')
print('Compressed file size:', getsize(outfile), 'bytes')
print(f'Compression rate: {(getsize(outfile) / getsize(infile)) * 100}')
