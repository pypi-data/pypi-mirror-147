
from concurrent.futures import thread
from ruamel.yaml import YAML
import sys
from pathlib import Path
from ruamel.yaml.main import round_trip_dump as yaml_dump
import subprocess
import os
from ploomber.spec import DAGSpec
from datetime import datetime
import uuid
import glob

script_setup='''# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

'''

def transform_pipeline(pipeline_file='pipeline.yaml', run_id=None, target_file=None, debug=False, meta={'extract_upstream': False}):
    extract_upstream = meta.get('extract_upstream', True)
    if run_id is None:
        run_id = 'view'
        
    yaml=YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
    pipeline_path = Path(pipeline_file)
    phases = yaml.load(pipeline_path.read_text())

    if phases is None:
        raise Exception('No tasks fown in pipeline')

    phase_keys = [x.strip() for x in 'steps, runs-on, needs, strategy, name'.split(',')]
    step_keys = [x.strip() for x in 'name, uses, run, with, matrix, needs'.split(',')]
    ploomber_steps = []
    prev_name = None
    stepid = 0
    for phase_key in phases:
        phase = phases[phase_key]

        for k in phase:
            if k not in phase_keys:
                raise Exception(f'Error: phase key {k}, expected one of {phase_keys}')

            if k == 'steps':
                phase_steps = phase.get('steps', [])
                
                for step in phase_steps:
                    stepid += 1
                    for step_prop in step:
                        if step_prop not in step_keys:
                            raise Exception(f'Error: step key {step_prop}, expected one of {step_keys}')

                    uses_function = step.get('uses', None)
                    step_name = step.get('name', uses_function.split('.')[-1] if uses_function is not None else f'_step_{stepid}')
                    
                    name = f'{phase_key}-{step_name}'
                    product_complete = f'.run-{run_id}-product-{name}_complete.txt'

                    run_code = step.get('run', None)
                    

                    if uses_function is not None:

                        ploomber_step = {
                            'source': uses_function,
                            'name': name,
                            'product': product_complete
                        }

                        params = step.get('with', None)
                        if params is not None:
                            ploomber_step['params'] = params


                        matrix = step.get('matrix', None)
                        if matrix is not None:
                            ploomber_step['grid'] = matrix

                    elif run_code is not None:
                        code_fn = pipeline_path.absolute().parent / f'.run-{run_id}-{name}.sh'
                        code_lines=script_setup.split('\n') + [x.rstrip() for x in run_code.split('\n')] + ['touch {{product}}']
                        code = '\n'.join(code_lines)
                        print(code_fn)
                        print(code)
                        code_fn.write_text(code)
                        ploomber_step = {
                            'source': str(code_fn),
                            'name': name,
                            'product': product_complete
                        }

                    # if not extract_upstream:
                    #     if prev_name is not None:
                    #         ploomber_step['upstream'] = [prev_name]

                    needs = step.get('needs', None)
                    if needs is not None:
                        ploomber_step['upstream'] = needs

                    ploomber_steps.append(ploomber_step)
                    prev_name = name

                    
    pp_file = target_file or f'.run-{run_id}-pp.yaml'
    pipeline_text = yaml_dump({ 
            'meta': meta,
            'executor':{'dotted_path': 'ploomber.executors.Serial'},
#             'executor':{'dotted_path': 'ploomber.executors.Parallel','processes': 2 },
            'tasks': ploomber_steps})
    
    Path(pipeline_path.absolute().parent / pp_file).write_text(pipeline_text)
    
    if debug:
        print(pipeline_text)


def build(pipeline_file='pipeline.yaml', run_id=None, env={}, status=False):
    intermediate_file='pp.yaml'
    if run_id is not None:
        intermediate_file=f'.run-{run_id}-pp.yaml'
    transform_pipeline(pipeline_file, run_id=run_id)

    spec = DAGSpec(intermediate_file, env=env)
    print(spec.env)
    dag = spec.to_dag()
    dag.build(force=True)
    if status:
        print(dag.status())
    
def make():    
    Path('requirements.dev.txt').write_text(['pytest', 'jupyter','jupyterlab'].join('\n'))
    Path('requirements.txt').write_text(['pandas', 'scikit-learn'].join('\n'))
    Path('pipeline.yaml').touch()
    Path('env.yaml').touch()
    
    
def run(env={}):
    try:
        run_id = str(uuid.uuid4())
        print(f'Run: {run_id}')
        start_time = datetime.now()
#         build(run_id=run_id, env={**env, 'run_id':run_id})
        build(run_id=run_id, env=env)
    finally:
        clean(run_id=run_id)
        pass

def delete_files(pattern):
    files = glob.glob(pattern)
    for f in files:
        Path(f).unlink()

def clean(run_id=None):
    if run_id is not None:
        delete_files(f'.run-{run_id}-*')
        delete_files(f'..run-{run_id}-*')
        # print(subprocess.check_output(f'rm -f .run-{run_id}-*', shell=True).decode())
        # print(subprocess.check_output(f'rm -f ..run-{run_id}-*', shell=True).decode())
    
