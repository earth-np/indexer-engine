from flask import Flask, jsonify
import threading
import time
from models import db, Balance,Config
from config import get_config
from logs import get_transfer_logs,get_web3

app = Flask(__name__)
app.config.from_object(get_config())

# Initialize database and create tables
db.connect()
db.create_tables([Balance,Config])

# Event to signal thread to stop
shutdown_event = threading.Event()

# Interval job function
def interval_job():
    time.sleep(3)
    while not shutdown_event.is_set():
        try:
            last_processed_block = Config.get(key="last_processed_block")
        except:
            last_processed_block = Config.create(key="last_processed_block",value=app.config['START_BLOCK'])
        
        last_processed_block_number = int(last_processed_block.value)
        
        current_block = get_web3().eth.block_number
        
        latest_block = min(current_block,last_processed_block_number+1000)
        
        print(f"Processing blocks {last_processed_block_number} to {latest_block}")
        transfers = get_transfer_logs(token_address=app.config['TOKEN_ADDRESS'],from_block=last_processed_block_number,to_block=latest_block)
        with db.atomic():
            for transfer in transfers:
                print(transfer)
                try:
                    balanceFrom = Balance.get(address=transfer.from_address)
                except:
                    balanceFrom = Balance.create(address=transfer.from_address,balance=0,updated_block=0)
                balanceFrom.address = transfer.from_address
                balanceFrom.balance = str(int(balanceFrom.balance) - (transfer.value))
                balanceFrom.updated_block = transfer.block_number
                balanceFrom.save()
                try:
                    balanceTo = Balance.get(address=transfer.to_address)
                except:
                    balanceTo = Balance.create(address=transfer.to_address,balance=0,updated_block=0)
                balanceTo.address = transfer.to_address
                balanceTo.balance = str(int(balanceTo.balance) + (transfer.value))
                balanceTo.updated_block = (transfer.block_number)
                balanceTo.save()
            last_processed_block.value = str(latest_block)
            last_processed_block.save()
        shutdown_event.wait(app.config['INTERVAL'])
    print("Interval job shutting down gracefully")

# Start the interval job in a separate thread
job_thread = threading.Thread(target=interval_job)
job_thread.daemon = True
job_thread.start()

# api route get address balance
@app.route('/api/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = Balance.get_or_none(address=address)
    if balance:
        return jsonify({"address": balance.address, "balance": balance.balance})
    else:
        return jsonify({"message": "Address not found"}), 404
    
#  health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})



def graceful_shutdown(signum, frame):
    print("Received shutdown signal. Initiating graceful shutdown...")
    shutdown_event.set()
    job_thread.join(timeout=app.config['INTERVAL'] * 2)
    print("Interval job has shut down. Exiting.")
    exit(0)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    app.run(debug=False)