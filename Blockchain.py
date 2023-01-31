import datetime
import hashlib
import json

from flask import Flask, jsonify


class Blockchain:
   def __init__(self):        #constroctuor of the object 
       self.chain = [] 
       self.create_blockchain(proof=1, previous_hash='0')  #first block proof=1 & hash=0
    
   def create_blockchain(self, proof, previous_hash):     
       block = {
           'index': len(self.chain) + 1,
           'timestamp': str(datetime.datetime.now()),
           'proof': proof,
           'previous_hash': previous_hash
       }
       self.chain.append(block)  #Add an element to the block list:
       
       return block

   def get_previous_block(self):
       last_block = self.chain[-1]
       return last_block

   def proof_of_work(self, previous_proof):
       # miners proof submitted
       new_proof = 1
       # this is the status of proof of work
       check_proof_of_work = False
       while check_proof_of_work is False:
           # this algorithm depend on the previous proof and new proof
           hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
           # checking the solution to problem, by using proof in cryptographic encryption
           # if proof results in 4 leading zero's in the hash operation, then: it is valid
           if hash_operation[:4] == '0000':
               check_proof_of_work = True
           else:
               # if  solution is wrong, trying another chance until correct
               new_proof += 1
       return new_proof

   def hash(self, block):    # generate a hash of block
       encoded_block = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(encoded_block).hexdigest()

   def is_chain_valid(self, chain):   # checking if the chain is  or not 
       # Stage one we need to check if the current block has the same hash of the prvious one 
       # make the first block in the chain as the previous block
       previous_block = chain[0]
       # an index of the blocks in the chain for iteration
       block_index = 1
       while block_index < len(chain):
           # get the current block
           block = chain[block_index]
           # checking the hashes if they are equal 
           if block["previous_hash"] != self.hash(previous_block):
               return False
           # Stge two checking the proof
           # get the previous proof from the previous block
           previous_proof = previous_block['proof']

           # get the current proof from the current block
           current_proof = block['proof']

           # run the proof data through the algorithm
           hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
           # check if hash operation is invalid
           if hash_operation[:4] != '0000':
               return False
           # set the previous block to the current block after running validation on current block
           previous_block = block
           block_index += 1
       return True


app = Flask(__name__)

blockchain = Blockchain()


@app.route('/block_mays', methods=['GET'])
def block_mays():
   # get the data we need to create a block
   previous_block = blockchain.get_previous_block()
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)
   previous_hash = blockchain.hash(previous_block)
   block = blockchain.create_blockchain(proof, previous_hash)
   response = [ 
                {'Message': 'Mays_Block!'}, {'Index' : block['index']},
                {'Timestamp': block['timestamp']}, {'Proof': block['proof']}, {'Previous_hash': block['previous_hash']}
              ]
   return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
   response = {
               'MaysChain': blockchain.chain,
               'Length': len(blockchain.chain)                     
               }
   return jsonify(response), 200   

app.run(host='0.0.0.0', port=5000)