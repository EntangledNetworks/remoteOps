# ====================================================== #
# >>> Definitions for various remote operation units <<< #
# >>>      written for QISkit circuit objects        <<< #
# ====================================================== #

import qiskit.circuit as qc

def get_cregs(circ, creg):
    '''
    Utility to test if circ has creg.
    If it doesn't, append one to circ such that
    EPR-mediated operations can occur.
    Args:
        circ: A QuantumCircuit object
        creg: Either a ClassicalRegister object, or name string.
    Returns:
        creg: A ClassicalRegister object.
    Side-effects:
        creg appended to circ.
    '''
    reg_added = False
    if type(creg)==str:
        # If we're given a creg NAME as string
        has_creg = circ.has_register(qc.ClassicalRegister(2,creg))
    else:
        # Otherwise, assume creg is given as a ClassicalRegister
        has_creg = circ.has_register(creg)

    if creg==None or not has_creg:
        reg_added = True
        creg = qc.ClassicalRegister(2,'c_epr')
        circ.add_register(creg)
    
    return creg, reg_added

def get_qregs(circ, qreg):
    '''
    Utility to test if circ has creg.
    If it doesn't, append one to circ such that
    EPR-mediated operations can occur.
    Args:
        circ: A QuantumCircuit object
        qreg: Either a QuantumRegister object, or name string.
    Returns:
        qreg: A QuantumRegister object.
    Side-effects:
        qreg appended to circ.
    '''
    reg_added = False
    if type(qreg)==str:
        # If we're given a qreg NAME as string
        has_qreg = circ.has_register(qc.QuantumRegister(2,qreg))
    else:
        # Otherwise, assume qreg is given as a QuantumRegister
        has_qreg = circ.has_register(qreg)

    if qreg==None or not has_qreg:
        reg_added = True
        qreg = qc.QuantumRegister(2,'q_epr')
        circ.add_register(qreg)
    
    return qreg, reg_added
        

def setAncilla(circ, epr0, epr1, creg=None):
    '''
    Set EPR state on bus.
    '''
    circ.h(epr0)
    circ.cnot(epr0,epr1)
    

def buildRemoteCRZ(circ, phi, ctrl, targ, epr0, epr1, creg):
    '''
    Builds a remote controlled-Rz(phi)

    Args:
        circ: A QISkit circuit object
        ctrl: Control qubit
        targ: Target qubit
        phi: Real parameter for CRZ
        epr_creg: creg or creg name string, for EPR operations
        epr_qreg: qreg or qreg name string, for EPR operations
    '''
    # Perform EPR-mediated CRZ operation
    circ.rz(phi/2,ctrl)
    circ.rz(phi/2,targ)

    circ.cnot(ctrl,epr0)
    circ.measure(epr0,creg[0])
    circ.x(epr1).c_if(creg[0],1)

    circ.cnot(targ,epr1)
    circ.rz(-phi/2,epr1)

    circ.h(epr1)
    circ.measure(epr1,creg[1])

    circ.z(ctrl).c_if(creg[1],1)
    circ.z(targ).c_if(creg[1],1)


def buildRemoteZZ(circ, phi, qb1, qb2, epr0, epr1, creg):
    '''
    Builds a remote ZZ gate

    Args:
        circ: A QISkit circuit object
        qb1, qb2: Qubits acted on by ZZ gate
        phi: Real parameter for ZZ gate
        epr_creg: creg or creg name string, for EPR operations
        epr_qreg: qreg or qreg name string, for EPR operations
    '''
    # Perform Remote-ZZ gate
    circ.cnot(qb1,epr0)
    circ.cnot(qb2,epr1)

    circ.measure(epr0,creg[0])
    circ.x(epr1).c_if(creg[1],1)

    circ.rz(phi,epr1)
    circ.h(epr1)
    circ.measure(epr1,creg[1])

    circ.z(qb1).c_if(creg[1],1)
    circ.z(qb2).c_if(creg[1],1)

    circ.x(epr0).c_if(creg[0],1)
    circ.x(epr1).c_if(creg[1],1)


def buildRemoteCX(circ, ctrl, targ, epr0, epr1, creg):
    '''
    Builds a remote CNOT gate

    Args:
        circ: A QISkit circuit object
        ctrl: Control qubit
        targ: Target qubit
        epr_creg: creg or creg name string, for EPR operations
        epr_qreg: qreg or qreg name string, for EPR operations
    '''
    # Remote CX ops
    circ.cnot(ctrl,epr0)
    circ.cnot(epr1,targ)

    circ.measure(epr0,creg[0])
    circ.x(epr1).c_if(creg[0],1)
    circ.x(targ).c_if(creg[0],1)
    circ.h(epr1)
    circ.measure(epr1,creg[1])
    circ.z(ctrl).c_if(creg[1],1)

    circ.x(epr0).c_if(creg[0],1)
    circ.x(epr1).c_if(creg[1],1)


def buildTeleportation(circ, source, targ, epr0, epr1, creg):
    '''
    Build a teleportation circuit.
    Uses teleportation to move a qubit from source to targ.

    Args:
        circ: A QISkit circuit object
        source: Source qubit
        targ: Target qubit
        epr_creg: creg or creg name string, for EPR operations
        epr_qreg: qreg or qreg name string, for EPR operations
    '''
    # Insert teleportation operations.
    circ.cnot(source,epr0)
    circ.h(source)

    circ.measure(source,creg[0])
    circ.measure(epr0,creg[1])
    circ.x(epr1).c_if(creg[1],1)
    circ.z(epr1).c_if(creg[0],1)

    circ.x(source).c_if(creg[0],1)
    circ.x(epr0).c_if(creg[1],1)

    circ.swap(epr1,targ)

 
def addInstr(circ, name, qb1=None, qb2=None, params=[], epr_creg=None, epr_qreg=None):
    '''
    Convenience method to add custom instructions.

    This adds custom named instruction object into a QISkit circuit,
    that can later be decomposed into a set of more basic operations.
    Currently, various two-qubit operations are supported (see above).

    An extra (size 2) qreg and creg can be provided, to facilitate
    EPR-mediated operations. If omitted, this method will add one.
    Generally, qb1 "talks directly to" epr_qreg[0] and qb2 to epr_qreg[1].

    Args:
        circ: A QISkit circuit object
        name: Str, names the new instruction.
        qb1,qb2: Qubits targeted by the custom instruction.
        params: List, specifies any relevant params for the instruction.
        epr_qreg: Extra qreg to hold and facilitate EPR operations.
        epr_creg: Companion creg for EPR operations.
    Returns:
        circ: An updated QISkit circuit with the named instruction added.
    '''
    
    # If a creg/qreg isn't specified for EPR operation, add it.
    creg, _ = get_cregs(circ, epr_creg)
    qreg, _ = get_qregs(circ, epr_qreg)

    instrSet = {
        'RemoteCX':    qc.Instruction('RemoteCX', 4, 2, params),
        'RemoteRZZ':   qc.Instruction('RemoteRZZ',4, 2, params),
        'RemoteCRZ':   qc.Instruction('RemoteCRZ',4, 2, params),
        'Teleport':    qc.Instruction('Teleport', 4, 2, params),
        'GenEPR':      qc.Instruction('GenEPR',  2, 0, params)
    }

    qargs = [qb1, qb2, qreg[0], qreg[1]]
    circ.append(instrSet['GenEPR'], qreg, [])
    if name!='GenEPR':
        try:
            circ.append(instrSet[name], qargs, creg)
        except:
            raise BaseException("Undefined instruction!")


def decompose(circ, gates=['RemoteCX','RemoteRZZ','RemoteCRZ','Teleport','GenEPR']):
    '''
    Replace custom instructions with basic QISkit ops.
    '''
    circuitChunks = []
    emptyCirc = circ.copy()
    emptyCirc.data = []
    idx = 0

    idxStart = 0
    tempCirc = emptyCirc.copy()
    for idx,op in enumerate(circ.data):
        obj = op[0]
        if obj.name in gates:
            circuitChunks.extend(circ[idxStart:idx])
            idxStart = idx+1

            args = op[0].params+op[1]+[op[2]]
            
            if obj.name=='RemoteCX':
                buildRemoteCX(tempCirc,*args)
            elif obj.name=='RemoteRZZ':
                buildRemoteZZ(tempCirc,*args)
            elif obj.name=='RemoteCRZ':
                buildRemoteCRZ(tempCirc,*args)
            elif obj.name=='Teleport':
                buildTeleportation(tempCirc,*args)
            elif obj.name=='GenEPR':
                setAncilla(tempCirc,*args)
            
            circuitChunks.extend(tempCirc)
            tempCirc = emptyCirc.copy()
    
    circuitChunks.extend(circ[idxStart:])
    
    circ.data = circuitChunks

def autosubstitute(circ, reglist, gates=['cx'], epr_qreg=None, epr_creg=None):
    '''
    Scans input circ, and replace any operations listed in
    'gates' that happens to straddle different registers
    (as specified in 'reglist') with their EPR-mediated
    counterpart.
    '''
    # If a creg/qreg isn't specified for EPR operation, add it.
    creg, _ = get_cregs(circ, epr_creg)
    qreg, _ = get_qregs(circ, epr_qreg)

    circuitChunks = []
    emptyCirc = circ.copy()
    emptyCirc.data = []
    idx = 0

    idxStart = 0
    tempCirc = emptyCirc.copy()
    for idx,op in enumerate(circ.data):
        obj = op[0]
        if len(op[1])==2: # Two qargs indicating 2-qb gate.
            # Check if qargs are in reglist given.
            # Only proceed if they are.
            substitute = False
            if op[1][0] in reglist[0] and op[1][1] in reglist[1]:
                substitute = True
            elif op[1][1] in reglist[0] and op[1][0] in reglist[1]:
                substitute = True

            if obj.name in gates and substitute==True:
                circuitChunks.extend(circ[idxStart:idx])
                idxStart = idx+1
                
                if obj.name=='cx':
                    addInstr(tempCirc, 'RemoteCX', op[1][0], op[1][1], [], creg, qreg)
                
                circuitChunks.extend(tempCirc)
                tempCirc = emptyCirc.copy()
    
    circuitChunks.extend(circ[idxStart:])
    
    circ.data = circuitChunks