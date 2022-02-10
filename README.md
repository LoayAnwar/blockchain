# blockchain

## Dependencies
Only python3 is needed to run this program

## Usage

Use this command to run the program.

```bash
foo@bar:~$ python3 blockchain.py
```

For simulating legit block chain enter 1

- The system will output the index of the block, previous block hash and the time the block was created.

For simulating a block chain attack enter 2 and enter the attacker computational power percentage

- If the attacker's chain gets 5 blocks longer than the honest chain, the attack is then called successful and the simulation stops.
- If the honest chain gets 5 blocks longer than the attacker's chain, the attacker is then notified. They can keep trying or stop the program if they choose to give up.

