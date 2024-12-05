import numpy as np
import plotly.graph_objects as go

def sph_to_cart(r, th, phi):
        #th = th + np.pi/2
        #phi +=np.pi
        #th = np.deg2rad(th); phi = np.deg2rad(phi)
        x = r*np.sin(th)*np.cos(phi)
        y = r*np.sin(th)*np.sin(phi)
        z = r*np.cos(th)

        return [x, y, z]
    
def cart_to_sph(x, y, z):

    r = np.sqrt(x**2+y**2+z**2)
    theta = (np.arccos(z/r))
    phi = ((np.arctan2(y, x) + 2 * np.pi) % (2 * np.pi))

    return [r, theta, phi]
    
def rot_mat(axis, angle):
        
        c = np.cos(angle); s = np.sin(angle)
        C= 1-c
        x = axis[0]; y = axis[1]; z = axis[2]

        matrix = [[ x*x*C+c,    x*y*C-z*s,  x*z*C+y*s ],
                  [ y*x*C+z*s,  y*y*C+c,    y*z*C-x*s ],
                  [ z*x*C-y*s,  z*y*C+x*s,  z*z*C+c   ]]

        return matrix

def rot_axis_angle(v1, v2):

    N_unit = np.cross(v1, v2)/np.linalg.norm(np.cross(v1,v2))
    v1_unit = v1/np.linalg.norm(v1)
    b_unit = np.cross(v1_unit, N_unit)
    z_unit = [0, 0, 1]
    c = cos_angle = np.dot(N_unit, z_unit)/(np.linalg.norm(N_unit)*np.linalg.norm(z_unit))
    angle = np.arccos(c)
    axis = np.cross(N_unit, z_unit)/(np.linalg.norm(np.cross(N_unit, z_unit)))

    return [axis, angle]

def rotate_to_xy(v1, v2):

    rot_ax, angle = rot_axis_angle(v1, v2)

    matrix = rot_mat(rot_ax, angle)
    v1_xy = np.dot(matrix, v1); v2_xy = np.dot(matrix, v2)

    return [v1_xy, v2_xy]

def arc_on_xy(vertices_xy, num):

    v1_xy_sph = cart_to_sph(*vertices_xy[0])
    v2_xy_sph = cart_to_sph(*vertices_xy[1])
    r_arc = v1_xy_sph[0]

    if abs(v1_xy_sph[2] - v2_xy_sph[2]) > np.pi:

        if v1_xy_sph[2] < v2_xy_sph[2]:

            v1_xy_sph[2] += 2*np.pi
            theta_arc = np.linspace(v2_xy_sph[1], v1_xy_sph[1], num)
            phi_arc = np.linspace(v2_xy_sph[2], v1_xy_sph[2], num)

        else:

            v2_xy_sph[2] += 2*np.pi
            theta_arc = np.linspace(v2_xy_sph[1], v1_xy_sph[1], num)
            phi_arc = np.linspace(v2_xy_sph[2], v1_xy_sph[2], num)

    else:
        # r_arc = np.linspace(v1_xy_sph[0], v1_xy_sph[0],num)
        theta_arc = np.linspace(v1_xy_sph[1], v2_xy_sph[1], num)
        phi_arc = np.linspace(v1_xy_sph[2], v2_xy_sph[2], num)

    arc_xy = sph_to_cart(r_arc, theta_arc, phi_arc)

    return arc_xy

def tri_indices(simplices):
    #simplices is a numpy array defining the simplices of the triangularization
    #returns the lists of indices i, j, k

        return ([triplet[c] for triplet in simplices] for c in range(3))

def plotly_trisurf(x, y, z, simplices, face_color = 'blue', opacity = 0.9, plot_edges=None):
    #x, y, z are lists of coordinates of the triangle vertices 
    #simplices are the simplices that define the triangularization;
    #simplices  is a numpy array of shape (no_triangles, 3)
    #insert here the  type check for input data

    points3D=np.vstack((x,y,z)).T
    tri_vertices=map(lambda index: points3D[index], simplices)# vertices of the surface triangles     
    zmean=[np.mean(tri[:,2]) for tri in tri_vertices ]# mean values of z-coordinates of 
                                                      #triangle vertices
    min_zmean=np.min(zmean)
    max_zmean=np.max(zmean)
    I,J,K=tri_indices(simplices)

    triangles=go.Mesh3d(x=x, y=y, z=z, i=I, j=J, k=K, name='', color=face_color, opacity=opacity)

    if plot_edges is None:# the triangle sides are not plotted

        return [triangles]
    else:
        #define the lists Xe, Ye, Ze, of x, y, resp z coordinates of edge end points for each triangle
        #None separates data corresponding to two consecutive triangles
        lists_coord=[[[T[k%3][c] for k in range(4)]+[None] for T in tri_vertices] for c in range(3)]
        Xe, Ye, Ze=[reduce(lambda x,y: x+y, lists_coord[k]) for k in range(3)]

        #define the lines to be plotted
        lines=go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color= 'rgb(50,50,50)', width=1.5))

        return [triangles, lines]
