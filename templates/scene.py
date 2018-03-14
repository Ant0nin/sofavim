import sys
import Sofa

class Scene_01 (Sofa.PythonScriptController):

    def _init_(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):
        self.logFile = "./log.txt"
        self.firstStep = True
        self.attachedTop = True

        rootNode.createObject('RequiredPlugin', pluginName='SuctionCup')
        rootNode.createObject('RequiredPlugin', pluginName='SoftRobots')

        rootNode.createObject('VisualStyle', displayFlags='showCollisionModels showInteractionForceFields hideVisualModels')

        # Global config
        rootNode.createObject('FreeMotionAnimationLoop')
        rootNode.createObject('GenericConstraintSolver', maxIterations='10000', tolerance='1e-3')
        rootNode.createObject('CollisionPipeline', verbose='0')
        rootNode.createObject('BruteForceDetection')
        rootNode.createObject('CollisionResponse', response='FrictionContact', responseParams='mu=0.6')
        rootNode.createObject('LocalMinDistance', alarmDistance='0.3', contactDistance='0.075', angleCone='0.01')

        # Suction cup params
        Config = {
            'InitialPosition' : '0 0 1',
            'TotalMass': '80',
            'YoungModulus': '700000',
            'PoissonRatio': '0.412031',
            'EdgesColor': '0 0.5 0.5',
            'WorldPosition': '0 0 10'
        }

        # Hierarchy
        SuctionCup = rootNode.createChild('SuctionCup')
        SuctionCup_Visual = SuctionCup.createChild('SuctionCup_Visual')
        SuctionCup_Collider = SuctionCup.createChild('SuctionCup_Collider')
        SuctionCup_OutsideSurf = SuctionCup.createChild('SuctionCup_OutsideSurf')
        SuctionCup_InsideSurf = SuctionCup.createChild('SuctionCup_InsideSurf')
        SuctionCup_Volume = SuctionCup.createChild('SuctionCup_Volume')
        Ground = rootNode.createChild('Ground')

        # Components
        SuctionCup.createObject('EulerImplicit') # maybe use RK4
        SuctionCup.createObject('SparseLDLSolver') # preconditioner
        SuctionCup.createObject('TetrahedronSetTopologyContainer', fileTopology='../meshes/suction_cup_2.vtk')
        SuctionCup.createObject('TetrahedronSetTopologyModifier')
        SuctionCup.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d')
        SuctionCup.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d', drawEdges="1", drawColorEdges=Config['EdgesColor'])
        SuctionCup.createObject('MechanicalObject', name='SuctionCup_Mech', translation=Config['InitialPosition'])
        SuctionCup.createObject('UniformMass', totalMass=Config['TotalMass'])
        SuctionCup.createObject('FastTetrahedralCorotationalForceField', method='large', poissonRatio=Config['PoissonRatio'], youngModulus=Config['YoungModulus'])
        SuctionCup.createObject('LinearSolverConstraintCorrection')

        SuctionCup_Collider.createObject('Mesh', filename='../meshes/suction_cup_2.obj')
        SuctionCup_Collider.createObject('MechanicalObject', name='SuctionCup_Collider', translation=Config['InitialPosition'])
        #SuctionCup_Collider.createObject('Triangle', selfCollision='false')
        #SuctionCup_Collider.createObject('Line', selfCollision='false')
        SuctionCup_Collider.createObject('Point', selfCollision='false')
        SuctionCup_Collider.createObject('BarycentricMapping', input='@..', output='@SuctionCup_Collider')

        SuctionCup_OutsideSurf.createObject('Mesh', name='SuctionCup_OutsideMesh', filename='../meshes/suction_cup_2_outside.obj')
        SuctionCup_OutsideSurf.createObject('MechanicalObject', name='SuctionCup_Outside', translation=Config['InitialPosition'])
        SuctionCup_OutsideSurf.createObject('Triangle', selfCollision='false')
        SuctionCup_OutsideSurf.createObject('AtmosphericPressureForceField', triangleList='@SuctionCup_OutsideMesh.triangles', showForces='1', normal='0 0 1', dmin="0.049", dmax="0.051", pressure="0 0 -2015")
        SuctionCup_OutsideSurf.createObject('BarycentricMapping', input='@..', output='@SuctionCup_Outside')

        SuctionCup_InsideSurf.createObject('Mesh', name='SuctionCup_InsideMesh', filename='../meshes/suction_cup_2_inside.obj')
        SuctionCup_InsideSurf.createObject('MechanicalObject', name='SuctionCup_Inside', translation=Config['InitialPosition'])
        SuctionCup_InsideSurf.createObject('Triangle', selfCollision='false')
        SuctionCup_InsideSurf.createObject('AtmosphericPressureForceField', triangleList='@SuctionCup_InsideMesh.triangles', showForces='1', normal='0 0 1', dmin="0.049", dmax="0.051", pressure="0 0 100") #TODO: Use CavityPressureForceField instead
        SuctionCup_InsideSurf.createObject('BarycentricMapping', input='@..', output='@SuctionCup_Inside')

        SuctionCup_Visual.createObject('OglModel', name='SuctionCup_Ogl', fileMesh='../meshes/suction_cup_2.obj', translation=Config['InitialPosition'])
        SuctionCup_Visual.createObject('BarycentricMapping', input='@../SuctionCup_Mech',  output='@SuctionCup_Ogl')
        
        SuctionCup_Volume.createObject('OglModel', name='SuctionCup_Volume', fileMesh='../meshes/suction_cup_2_volume.obj', translation=Config['InitialPosition'])
        SuctionCup_Volume.createObject('BarycentricMapping', input='@../SuctionCup_Mech', output='@SuctionCup_Volume')
        SuctionCup_Volume.createObject('MeshVolumeEngine', visualModel='@SuctionCup_Volume') #TODO: rename component? TODO: move bottom vertex of volume mesh
        #SuctionCup_Volume.createObject('VolumeFromTriangles')

        Ground.createObject('Mesh', filename='../meshes/plane.obj')
        Ground.createObject('MechanicalObject', name='Ground_Mech')
        Ground.createObject('Triangle', simulated=0, moving=0) # do not use T prefix because no TriangleTopology component
        Ground.createObject('Line', simulated=0, moving=0)
        Ground.createObject('Point', simulated=0, moving=0)
        Ground.createObject('OglModel', filename='../meshes/plane.obj')
        Ground.createObject('FixedConstraint', fixAll=1)

        return 0;
    
    def onBeginAnimationStep(self, deltaTime):
        return 0;

    def onMouseButtonLeft(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Left mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onKeyReleased(self, c):
        ## usage e.g.
        #if c=="A" :
        #    print "You released a"
        return 0;

    def initGraph(self, node):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onKeyPressed(self, c):
        ## usage e.g.
        #if c=="A" :
        #    print "You pressed control+a"
        return 0;

    def onMouseWheel(self, mouseX,mouseY,wheelDelta):
        ## usage e.g.
        #if isPressed : 
        #    print "Control button pressed+mouse wheel turned at position "+str(mouseX)+", "+str(mouseY)+", wheel delta"+str(wheelDelta)
        return 0;

    def storeResetState(self):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /home/abernard/workspace/imagine_hdd_prototype//home/abernard/workspace/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

def createScene(rootNode):
    rootNode.findData('dt').value = '0.005'
    rootNode.findData('gravity').value = '0 0 -9.81'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myscene = Scene_01(rootNode,commandLineArguments)
    return 0;
