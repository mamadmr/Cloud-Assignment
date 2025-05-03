from tasks import start_ctf_container, stop_ctf_container

res = start_ctf_container.delay("pwn_challenge", container_name="pwn1")
print(res.get(timeout=15))


stop_res = stop_ctf_container.delay(res.get()['container_id'])
print(stop_res.get(timeout=15))
