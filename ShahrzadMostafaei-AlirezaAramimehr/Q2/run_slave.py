from multiprocessing import Process, Queue
import subprocess


def slave_worker(slave_id, input_data, output_queue):
    """Worker function for each slave process"""
    proc = subprocess.run(
        ['python3', 'slave1.py'],
        input=input_data,
        text=True,
        capture_output=True
    )
    output_queue.put((slave_id, proc.stdout, proc.stderr))


if __name__ == '__main__':
    output_queue = Queue()
    processes = []
   


    for slave_id, input_data in zip([1, 2, 3], ["p1", "p2", "p3"]):
        p = Process(
            target=slave_worker,
            args=(slave_id, input_data, output_queue)
        )
        p.start()
        processes.append(p)
   


    for _ in processes:
        slave_id, out, err = output_queue.get()
        print(f"\nSlave {slave_id} results:")
        print(f"Output: {out.strip()}")
        if err:
            print(f"Errors: {err.strip()}")


    for p in processes:
        p.join()


    print("\nAll slaves completed!")

