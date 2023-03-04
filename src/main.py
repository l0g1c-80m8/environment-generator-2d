# sys imports
import os
import threading

# lib imports
from tqdm import tqdm

# local imports
from environment import *


def spawn_env(env_params, chunk_lims, envs_holder):
    for ctr in range(chunk_lims[1]):
        envs_holder[chunk_lims[0] + ctr] = EnvironmentDescriptor(
            environment_range=env_params['grid_range'],
            obstacle_point_range=env_params['obstacle_range'],
            start_point=env_params['start_point'],
            end_point=env_params['end_point'],
            obstacle_points=env_params['obstacle_points'],
            eta=env_params['eta'],
            grid_resolution=env_params['grid_resolution'],
            seed=(env_params['prng_seed'] + chunk_lims[0] + ctr),
            gamma=env_params['gamma']
        )


if __name__ == '__main__':
    # define params/consts for program
    ENVS_TO_GEN = 100
    OUT_DIR = '../out'

    # define the params for the environment
    params = dict()
    params['grid_range'] = (-1.2, 1.2)
    params['obstacle_range'] = (-0.7, 0.7)
    params['start_point'] = (-1, -1)
    params['end_point'] = (1, 1)
    params['obstacle_points'] = 15
    params['eta'] = 0.9
    params['grid_resolution'] = 500
    params['prng_seed'] = 1337
    params['gamma'] = 25

    # exec params/consts for defining the workers
    CHUNK_SIZE = math.ceil(ENVS_TO_GEN / os.cpu_count())
    N_CHUNKS = math.ceil(ENVS_TO_GEN / CHUNK_SIZE)

    # create workers to generate the environments and holder to store results
    envs = [None] * ENVS_TO_GEN
    workers = list(map(
        lambda chunk_lims: threading.Thread(
            target=spawn_env,
            args=(params, chunk_lims, envs)
        ),
        list(map(
            lambda chunk_num: (
                chunk_num * CHUNK_SIZE,
                (min(ENVS_TO_GEN, (chunk_num + 1) * CHUNK_SIZE)) - (chunk_num * CHUNK_SIZE)
            ),
            range(N_CHUNKS)
        ))
    ))

    # start workers
    for worker in workers:
        worker.start()

    # wait for all workers to finish
    for worker in workers:
        worker.join()

    # after collecting all envs, save them
    with tqdm(total=ENVS_TO_GEN) as pbar:
        for idx, env in enumerate(envs):
            env.save_env_img('{}/env-{}.png'.format(OUT_DIR, idx + 1))
            pbar.update(1)

    # exit without error
    exit(0)
