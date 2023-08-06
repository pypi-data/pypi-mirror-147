import numpy as np
import pyvista as pv
import vtk
from .implicit.implicit import surface
from .branch_addition.check import *
from .branch_addition.close import *
from .branch_addition.basis import *
from .branch_addition.calculate_length import *
from .branch_addition.calculate_radii import *
from .branch_addition.set_root import *
from .branch_addition.add_edge import *
from .branch_addition.add_bifurcation import *
from .branch_addition.add_branches_v3 import *
from .sv_interface.get_sv_data import *
from .sv_interface.options import *
from .sv_interface.build_files import *
from .sv_interface.waveform import generate_physiologic_wave
from copy import deepcopy
from itertools import combinations
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt

class tree:
    """
    Data structure:\n
    index: 0:2   -> proximal node coordinates \n
    index: 3:5   -> distal node coordinates \n
    index: 6:8   -> unit basis U (all) \n
    index: 9:11  -> unit basis V (all) \n
    index: 12:14 -> unit basis W (axial direction) (all) \n
    index: 15,16 -> children (-1 means no child) \n
    index: 17    -> parent (NA) \n
    index: 18    -> proximal node index (only real edges) \n
    index: 19    -> distal node index (only real edges) \n
    index: 20    -> length (path length) \n
    index: 21    -> radius (what are the units?) \n
    index: 22    -> flow (NA) \n
    index: 23    -> left bifurcation (NA) \n
    index: 24    -> right bifurcation (NA) \n
    index: 25    -> reduced resistance (NA) \n
    index: 26    -> depth (NA) \n
    index: 27    -> reduced downstream length (NA) \n
    index: 28    -> root radius scaling factor (same as edge for intermediate) \n
    index: 29    -> edge that subedge belongs to (if actual edge; self pointer) \n
    index: 30    -> self identifying index (-1 if intermediate) \n
    """
    def __init__(self):
        #self.parameters = {'gamma'   : 3.0,
        #                   'lambda'  : 2.0,
        #                   'mu'      : 1.0,
        #                   'nu'      : 3.6/100,
        #                   'Pperm'   : 100*1333.22,
        #                   'Pterm'   : 60*1333.22,
        #                   'Qterm'   : (0.125)/60,
        #                   'edge_num': 0}
        self.set_parameters()
        self.data = np.zeros((1,31))
        self.radius_buffer = 0.01
        self.fraction = None
        self.set_assumptions()
        self.rng_points = []
        self.time = {'search':[],
                     'constraints':[],
                     'local_optimize':[],
                     'collision':[],
                     'close_time':[],
                     'search_1':[],
                     'search_2':[],
                     'search_3':[],
                     'search_4':[],
                     'add_time':[],
                     'add_1':[],
                     'add_2':[],
                     'add_3':[],
                     'add_4':[],
                     'total':[]}

    def set_parameters(self,**kwargs):
        self.parameters = {}
        self.parameters['gamma']    = kwargs.get('gamma',3.0)
        self.parameters['lambda']   = kwargs.get('lambda',2.0)
        self.parameters['mu']       = kwargs.get('mu',1.0)
        self.parameters['nu']       = kwargs.get('nu',3.6)/100
        self.parameters['Pperm']    = kwargs.get('Pperm',100)*1333.22
        self.parameters['Pterm']    = kwargs.get('Pterm',60)*1333.22
        self.parameters['Qterm']    = kwargs.get('Qterm',0.125)/60
        self.parameters['edge_num'] = kwargs.get('edge_num',0)

    def set_assumptions(self,**kwargs):
        self.homogeneous = kwargs.get('homogeneous',True)
        self.directed    = kwargs.get('directed',False)
        self.convex      = kwargs.get('convex',False)
        self.hollow      = kwargs.get('hollow',False)
        self.dimension   = kwargs.get('dimension',3)
        self.clamped_root= kwargs.get('clamped_root',False)
        self.nonconvex_counter = 0

    def show_assumptions(self):
        print('homogeneous : {}'.format(self.homogeneous))
        print('directed    : {}'.format(self.directed))
        print('convex      : {}'.format(self.convex))
        print('hollow      : {}'.format(self.hollow))
        print('dimension   : {}'.format(self.dimension))
        print('clamped root: {}'.format(self.clamped_root))

    def set_boundary(self,boundary):
        self.boundary = boundary
        self.fraction = (self.boundary.volume**(1/3))/20

    def set_root(self,low=-1,high=0,start=None,direction=None,
                 limit_high=None,limit_low=None,niter=200):
        Qterm = self.parameters['Qterm']
        gamma = self.parameters['gamma']
        nu    = self.parameters['nu']
        Pperm = self.parameters['Pperm']
        Pterm = self.parameters['Pterm']
        result = set_root(self.data,self.boundary,Qterm,
                          gamma,nu,Pperm,Pterm,self.fraction,
                          self.homogeneous,self.convex,self.directed,
                          start,direction,limit_high,limit_low,self.boundary.volume,
                          low=-1,high=0,niter=niter)
        self.data = result[0]
        self.sub_division_map = result[1]
        self.sub_division_index = result[2]
        self.parameters['edge_num'] = 1
        #self.sub_division_map = [-1]
        #self.sub_division_index = np.array([0])

    def add(self,low,high,isforest=False):
        vessel,data,sub_division_map,sub_division_index = add_branch(self,low,high,threshold_exponent=0.5,
                                                                     threshold_adjuster=0.75,all_max_attempts=40,
                                                                     max_attemps=3,sampling=20,max_skip=8,
                                                                     flow_ratio=None)
        if isforest:
            return vessel,data,sub_division_map,sub_division_index
        else:
            self.data = data
            self.parameters['edge_num'] += 2
            self.sub_division_map = sub_division_map
            self.sub_division_index = sub_division_index

    def n_add(self,n):
        self.rng_points,_ = self.boundary.pick(size=40*n,homogeneous=True)
        self.rng_points = self.rng_points.tolist()
        #for i in tqdm(range(n),desc='Adding vessels'):
        for i in range(n):
            #self.rng_points = self.rng_points.tolist()
            self.add(-1,0)

        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['search'][1:],label='search time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['constraints'][1:],label='constraint time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['local_optimize'][1:],label='local time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['collision'][1:],label='collision time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['search_1'][1:],label='search 1 time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['search_2'][1:],label='search 2 time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['search_3'][1:],label='search 3 time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['search_4'][1:],label='search 4 time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['close_time'][1:],label='close_time time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['add_time'][1:],label='add_time')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['add_1'][1:],label='add_1')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['add_2'][1:],label='add_2')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['add_3'][1:],label='add_3')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['add_4'][1:],label='add_4')
        #plt.plot(list(range(len(self.time['search'][1:]))),self.time['total'][1:],label='total')
        #plt.ylim([0,0.1])
        #plt.legend()
        #plt.show()

    def show(self,surface=False,vessel_colors='red',background_color='white',
             resolution=100,show_segments=True,save=False,name=None,show=True):
        models = []
        actors = []
        colors = vtk.vtkNamedColors()
        if show_segments:
            if self.homogeneous:
                data_subset = self.data[self.data[:,-1] > -1]
            else:
                data_subset = self.data[self.data[:,29] > -1]
            for edge in range(data_subset.shape[0]):
                center = tuple((data_subset[edge,0:3] + data_subset[edge,3:6])/2)
                radius = data_subset[edge,21]
                direction = tuple(data_subset[edge,12:15])
                vessel_length = data_subset[edge,20]
                cyl = vtk.vtkTubeFilter()
                line = vtk.vtkLineSource()
                line.SetPoint1(data_subset[edge,0],data_subset[edge,1],data_subset[edge,2])
                line.SetPoint2(data_subset[edge,3],data_subset[edge,4],data_subset[edge,5])
                cyl.SetInputConnection(line.GetOutputPort())
                cyl.SetRadius(radius)
                cyl.SetNumberOfSides(resolution)
                models.append(cyl)
                mapper = vtk.vtkPolyDataMapper()
                actor  = vtk.vtkActor()
                mapper.SetInputConnection(cyl.GetOutputPort())
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(colors.GetColor3d(vessel_colors))
                actors.append(actor)
            if surface:
                mapper = vtk.vtkPolyDataMapper()
                actor  = vtk.vtkActor()
                mapper.SetInputData(self.boundary.polydata)
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(colors.GetColor3d('red'))
                actor.GetProperty().SetOpacity(0.25)
                actors.append(actor)
                for other_surface in self.boundary.subtracted_volumes:
                    mapper = vtk.vtkPolyDataMapper()
                    actor  = vtk.vtkActor()
                    mapper.SetInputData(other_surface.polydata)
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetColor(colors.GetColor3d('blue'))
                    actor.GetProperty().SetOpacity(0.5)
                    actors.append(actor)
            renderer = vtk.vtkRenderer()
            renderer.SetBackground(colors.GetColor3d(background_color))

            render_window = vtk.vtkRenderWindow()
            render_window.AddRenderer(renderer)
            render_window.SetWindowName('SimVascular Vessel Network')

            interactor = vtk.vtkRenderWindowInteractor()
            interactor.SetRenderWindow(render_window)

            for actor in actors:
                renderer.AddActor(actor)

            if save:
                render_window.Render()
                w2if = vtk.vtkWindowToImageFilter()
                w2if.SetInput(render_window)
                w2if.Update()

                writer = vtk.vtkPNGWriter()
                if name is None:
                    tag = time.gmtime()
                    name = str(tag.tm_year)+str(tag.tm_mon)+str(tag.tm_mday)+str(tag.tm_hour)+str(tag.tm_min)+str(tag.tm_sec)
                writer.SetFileName(os.getcwd()+os.sep+'{}.png'.format(name))
                writer.SetInputData(w2if.GetOutput())
                writer.Write()
            elif show==True:
                render_window.Render()
                interactor.Start()
            elif show==False:
                for m in models:
                    m.Update()
            return models

    def save(self,filename=None):
        if filename is None:
            tag = time.gmtime()
            filename = 'network_{}'.format(str(tag.tm_year)+
                                               str(tag.tm_mon) +
                                               str(tag.tm_mday)+
                                               str(tag.tm_hour)+
                                               str(tag.tm_min) +
                                               str(tag.tm_sec))
        os.mkdir(filename)
        file = open(filename+"/vessels.ccob",'wb')
        pickle.dump(self.data,file)
        file.close()
        file = open(filename+"/parameters.ccob",'wb')
        parameters = (self.parameters,self.fraction,self.homogeneous,self.directed,self.convex)
        pickle.dump(parameters,file)
        file.close()
        file = open(filename+"/boundary.ccob",'wb')
        pickle.dumps(self.boundary,file)
        file.close()

    def load(self,filename):
        file = open(filename+"/vessels.ccob",'rb')
        self.data = pickle.load(file)
        file.close()
        file = open(filename+"/parameters.ccob",'rb')
        self.parameters,self.fraction,self.homogeneous,self.directed,self.convex = pickle.load(file)
        file.close()
        file = open(filename+"/boundary.ccob",'rb')
        self.boundary = pickle.loads(file)
        file.close()

    def export(self,steady=True,apply_distal_resistance=True,gui=True):
        interp_xyz,interp_r,interp_n,frames,branches = get_interpolated_sv_data(self.data)
        points,radii,normals    = sv_data(interp_xyz,interp_r,radius_buffer=self.radius_buffer)
        if steady:
            time = [0, 1]
            flow = [self.data[0,22], self.data[0,22]]
        else:
            time,flow = generate_physiologic_wave(self.data[0,22],self.data[0,21]*2)
            time = time.tolist()
            flow = flow.tolist()
            flow[-1] = flow[0]
        if apply_distal_resistance:
            R = self.parameters['Pterm']/self.data[0,22]
        else:
            R = 0
        options = file_options(time=time,flow=flow,gui=gui,distal_resistance=R)
        build(points,radii,normals,options)

    def collision_free(self,outside_vessels):
        return no_outside_collision(self,outside_vessels)

class forest:
    def __init__(self,boundary=None,number_of_networks=1,
                 trees_per_network=[2],scale=None,start_points=None,
                 directions=None,root_lengths_high=None,
                 root_lengths_low=None,convex=False):
        self.networks    = []
        self.connections = []
        self.backup      = []
        self.boundary    = boundary
        self.convex      = convex
        self.number_of_networks = number_of_networks
        self.trees_per_network = trees_per_network
        if isinstance(start_points,type(None)):
            start_points = [[None for j in range(trees_per_network[i])] for i in range(number_of_networks)]
        if isinstance(directions,type(None)):
            directions = [[None for j in range(trees_per_network[i])] for i in range(number_of_networks)]
        if isinstance(root_lengths_high,type(None)):
            root_lengths_high = [[None for j in range(trees_per_network[i])] for i in range(number_of_networks)]
        if isinstance(root_lengths_low,type(None)):
            root_lengths_low = [[None for j in range(trees_per_network[i])] for i in range(number_of_networks)]
        self.starting_points = start_points
        self.directions = directions
        self.root_lengths_high = root_lengths_high
        self.root_lengths_low  = root_lengths_low

    def set_roots(self,scale=None,bounds=None):
        if self.boundary is None:
            print("Need to assign boundary!")
            return
        networks = []
        connections = []
        backup = []
        for idx in range(self.number_of_networks):
            network = []
            if not isinstance(self.trees_per_network,list):
                print("trees_per_network must be list of ints"+
                      " with length equal to number_of_networks")
            for jdx in range(self.trees_per_network[idx]):
                tmp = tree()
                tmp.set_assumptions(convex=self.convex)
                if self.directions[idx][jdx] is not None:
                    tmp.clamped_root = True
                tmp.set_boundary(self.boundary)
                if scale is not None:
                    tmp.parameters['Qterm'] *= scale
                if idx == 0 and jdx == 0:
                    collisions = [True]
                else:
                    collisions = [True]
                while any(collisions):
                    if bounds is None:
                        tmp.set_root(start=self.starting_points[idx][jdx],
                                     direction=self.directions[idx][jdx],
                                     limit_high=self.root_lengths_high[idx][jdx],
                                     limit_low=self.root_lengths_low[idx][jdx])
                    else:
                        print("Not implemented yet!")
                    collisions = []
                    for net in networks:
                        for t in net:
                            collisions.append(obb(t.data,tmp.data[0,:]))
                network.append(tmp)
            networks.append(network)
            connections.append(None)
            backup.append(None)
        self.networks    = networks
        self.connections = connections
        self.backup      = backup

    def add(self,number_of_branches,network_id=0,radius_buffer=0.01):
        if network_id == -1:
            exit_number = []
            active_networks = list(range(len(self.networks)))
            for network in self.networks:
                exit_number.append(network[0].parameters['edge_num'] + number_of_branches)
        else:
            exit_number = []
            active_networks = [network_id]
            exit_number.append(self.networks[network_id][0].parameters['edge_num'] + number_of_branches)
        while len(active_networks) > 0:
            for nid in active_networks:
                number_of_trees = len(self.networks[nid])
                for njd in range(number_of_trees):
                    success = False
                    while not success:
                        vessel,data,sub_division_map,sub_division_index = self.networks[nid][njd].add(-1,0,isforest=True)
                        new_vessels = np.vstack((data[vessel,:],data[-2,:],data[-1,:]))
                        repeat = False
                        for nikd in range(len(self.networks)):
                            if nikd == nid:
                                check_trees = list(range(len(self.networks[nikd])))
                                check_trees.remove(njd)
                            else:
                                check_trees = list(range(len(self.networks[nikd])))
                            for njkd in check_trees:
                                if not self.networks[nikd][njkd].collision_free(new_vessels):
                                    repeat = True
                                    break
                            if repeat:
                                break
                        if repeat:
                            continue
                        else:
                            success = True
                    self.networks[nid][njd].data = data
                    self.networks[nid][njd].parameters['edge_num'] += 2
                    self.networks[nid][njd].sub_division_map = sub_division_map
                    self.networks[nid][njd].sub_division_index = sub_division_index
                print(self.networks[nid][0].parameters['edge_num'])
                if self.networks[nid][0].parameters['edge_num'] >= exit_number[nid]:
                    active_networks.remove(nid)

    def export(self,show=True,resolution=100,final=False):
        model_networks = []
        for network in self.networks:
            model_trees = []
            for network_tree in network:
                model = []
                for edge in range(network_tree.parameters['edge_num']):
                    center = tuple((network_tree.data[edge,0:3] + network_tree.data[edge,3:6])/2)
                    radius = network_tree.data[edge,21]
                    direction = tuple(network_tree.data[edge,12:15])
                    vessel_length = network_tree.data[edge,20]
                    model.append(pv.Cylinder(radius=radius,height=vessel_length,
                                             center=center,direction=direction,
                                             resolution=resolution))
                model_trees.append(model)
            model_networks.append(model_trees)
        """
        model_connections = []
        for connections in conn:
            if connections is None:
                continue
            else:
                for c_idx in range(connections.shape[0]):
                    center = tuple((connections[c_idx,0:3] + connections[c_idx,3:6])/2)
                    radius = connections[c_idx,21]
                    direction = tuple((connections[c_idx,3:6] - connections[c_idx,0:3])/connections[c_idx,20])
                    vessel_length = connections[c_idx,20]
                    model_conn.append(pv.Cylinder(radius=radius,height=vessel_length,
                                                  center=center,direction=direction,
                                                  resolution=resolution))
        """
        if show:
            plot = pv.Plotter()
            colors = ['r','b','g','y']
            #plot.set_background(color=[253,250,219])
            for model_network in model_networks:
                for color_idx, model_tree in enumerate(model_network):
                    for model in model_tree:
                        plot.add_mesh(model,colors[color_idx])
            #for c_model in model_conn:
            #    plot.add_mesh(c_model,'r')
                #if i == 0:
                #    plot.add_mesh(model[i],'r')
                #else:
                #    plot.add_mesh(model[i],'b')
            #path = plot.generate_orbital_path(n_points=100,viewup=(1,1,1))
            #plot.show(auto_close=False)
            #plot.open_gif('cco_gamma.gif')
            #plot.orbit_on_path(path,write_frames=True)
            #plot.close()
            return plot

def perfusion_territory(tree,subdivisions=0,mesh_file=None,tree_file=None):
    terminals = tree.data[tree.data[:,15]<0,:]
    terminals = terminals[terminals[:,16]<0,:]
    territory_id = []
    territory_volumes = np.zeros(len(terminals))
    vol = tree.boundary.tet.grid.compute_cell_sizes().cell_data['Volume']
    #for idx, cell_center in tqdm(enumerate(tree.boundary.tet.grid.cell_centers().points),desc='Calculating Perfusion Territories'):
    for idx, cell_center in enumerate(tree.boundary.tet.grid.cell_centers().points):
        closest_terminal = np.argmin(np.linalg.norm(cell_center.reshape(1,-1)-terminals[:,3:6],axis=1))
        territory_id.append(closest_terminal)
        territory_volumes[closest_terminal] += vol[idx]
    territory_id = np.array(territory_id)
    tree.boundary.tet.grid['perfusion_territory_id'] = territory_id
    if mesh_file is not None:
        tree.boundary.tet.grid.save(mesh_file)
    else:
        tree.boundary.tet.grid.save('example.vtu')
    models = tree.show(show=False)
    append = vtk.vtkAppendPolyData()
    #append.UserManagedInputsOn()
    #append.SetInputDataObject(models[0])
    #append.SetNumberOfInputs(len(models))
    for i in range(len(models)):
        append.AddInputData(models[i].GetOutput())
    append.Update()
    total_tree = append.GetOutput()
    writer = vtk.vtkXMLPolyDataWriter()
    if tree_file is not None:
        writer.SetFileName(tree_file)
    else:
        writer.SetFileName(os.getcwd()+os.sep+'example_tree.vtp')
    writer.SetInputDataObject(total_tree)
    writer.Update()
    return territory_id,territory_volumes/np.sum(territory_volumes)
