###########################################################################
## A simple test script for AiiDA-ase with a set of simple set of         #
## parameters including QuasiNewton and PW operation mode with GPAW       #
###########################################################################

import sys
import os
from aiida import orm, engine

def main():

    ## Use the CalculationFactory for ASE
    ASECalculation = CalculationFactory('ase.ase')
    ## get the builder
    builder = ASECalculation.get_builder()

    ### Add in the code
    code = load_code('gpaw-ase@dtu_xeon8') ## Change the right code
    builder.code = code

    ### BaTiO3 cubic structure
    alat = 4. # angstrom
    cell = [[alat, 0., 0.,],
            [0., alat, 0.,],
            [0., 0., alat,],
            ]
    StructureData = DataFactory('structure')
    s = StructureData(cell=cell)
    s.append_atom(position=(0.,0.,0.),symbols=['Ba'])
    s.append_atom(position=(alat/2.,alat/2.,alat/2.),symbols=['Ti'])
    s.append_atom(position=(alat/2.,alat/2.,0.),symbols=['O'])
    s.append_atom(position=(alat/2.,0.,alat/2.),symbols=['O'])
    s.append_atom(position=(0.,alat/2.,alat/2.),symbols=['O'])
    builder.structure = s

    ### Kpoints for the 
    KpointsData = DataFactory('array.kpoints')
    kpoints = KpointsData()
    kpoints.set_kpoints_mesh([2,2,2])
    builder.kpoints = kpoints

    ### setup the parameters
    parameters = {"calculator": {"name":"gpaw",
                            "args":{"mode":{"@function":"PW",
                                            "args":{"ecut":300}
                            }}},
            'atoms_getters':["temperature"],
            'calculator_getters':[["potential_energy",{}]],
            'optimizer':{'name':'QuasiNewton',
                        'args':{},
                        'run_args':{"fmax":0.05},
                        }}
    builder.parameters = orm.Dict(dict=parameters)

    ### setup the labels and other book-keeping things
    # builder.label = 'Test calculation for GPAW'
    # builder.description = 'BaTiO3 ASE test calculation witH GPAW as a calculator'
    builder.metadata.options.resources = {'num_machines':1}
    builder.metadata.options.max_wallclock_seconds = 60 * 60
    builder.metadata.dry_run = True
    builder.metadata.store_provenance = False

    engine.submit(ASECalculation, **builder)



if __name__ == '__main__':
    main()