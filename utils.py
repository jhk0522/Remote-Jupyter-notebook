from ase.io.trajectory import Trajectory
from ase.visualize import view
import bisect
import numpy as np
import os
from subprocess import Popen, PIPE
import shutil
import matplotlib.pyplot as plt
from ase.calculators.vasp import xdat2traj


### set job environments
def que(file_name, node, cores):
    lines = open(file_name, 'r').readlines()
    lines[19] = node+'\n'
    lines[20] = cores+'\n'    
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

### job status, submit a job, get atoms and total energy
def job_status(directory, calc, atoms, print_energy = False, print_all_status = False):
    if os.path.isfile(directory+'/OUTCAR') == False:
        calc.calculate(atoms)
        with open(directory+'/vasp.out', 'r') as f:
            print(directory, ' : ' , f.readline().split()[2], ' has been submitted')
        te = None

    else:
        try:
            calc.read()
            atoms=calc.get_atoms()

            # check convergence
            if calc.converged == True:
                te = atoms.get_potential_energy()

                # want to print all que
                if print_all_status == True:

                    # kitchin's vasp doesn't have vasp.out
                    if os.path.isfile(directory+'/vasp.out') == False:
                        log = [output for output in os.listdir(directory) if output.startswith("|")]  # get log file
                        i=log[0].find('.o')

                        # want to print total energy
                        if print_energy == True:
                            print(directory, ' : ' , log[0][i+2:], ' was finished   | ', 'TE =',te)
                        # don't want to print total energy
                        else :
                            print(directory, ' : ' , log[0][i+2:], ' was finished')

                    # standard ase has vasp.out
                    else:
                        with open(directory+'/vasp.out', 'r') as f:
                            if print_energy == True:
                                print(directory, ' : ' , f.readline().split()[2], ' was finished   | ', 'TE =',te)

                            # don't want to print total energy
                            else:
                                print(directory, ' : ' , f.readline().split()[2], ' was finished')

            # if not converged
            else:
                # kitchin's vasp doesn't have vasp.out
                if os.path.isfile(directory+'/vasp.out') == False:
                    log = [output for output in os.listdir(directory) if output.startswith("|")]  # get log file
                    i=log[0].find('.o')
                    print(directory, ' : ' ,log[0][i+2:], ' queued or error')

                # standard ase has vasp.out
                else:
                    with open(directory+'/vasp.out', 'r') as f:
                        print(directory, ' : ' , f.readline().split()[2], ' queued or error')
                te = None
        # if calc.read doenst work for whatever reasons
        except:
            # kitchin's vasp doesn't have vasp.out
            if os.path.isfile(directory+'/vasp.out') == False:
                log = [output for output in os.listdir(directory) if output.startswith("|")]  # get log file
                i=log[0].find('.o')
                print(directory, ' : ' , log[0][i+2:], ' queued or error')
            else:
                with open(directory+'/vasp.out', 'r') as f:
                    print(directory, ' : ' , f.readline().split()[2], ' queued or error')
            te = None

    return atoms, te






