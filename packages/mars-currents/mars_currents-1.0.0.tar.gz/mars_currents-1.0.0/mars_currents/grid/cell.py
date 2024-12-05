import numpy as np
import plotly.graph_objects as go
from scipy.spatial import Delaunay
from . import grid_cell_geometry as gcm
import warnings


class Cell:
    
    def __init__(self, dr, dth, dphi, i, j, k, r, th, phi):
        
        self.dr = dr
        self.dth = dth 
        self.dphi = dphi 
        self.r_c = r[i]
        self.th_c = th[j] 
        self.phi_c = phi[k] 
        self.r_idx = i
        self.th_idx = j
        self.phi_idx = k
        self.r = r
        self.th = th 
        self.phi = phi
        self.neighbours = {'r':{-1:{None}, +1:{None}}, 
                          'th':{-1:{None}, +1:{None}}, 
                         'phi':{-1:{None}, +1:{None}}}
        
    def set_r_bin(self, r_bin):
        self.r_bin = r_bin
    
    def set_th_bin(self, th_bin):
        self.th_bin = th_bin
        
    def set_phi_bin(self, phi_bin):
        self.phi_bin = phi_bin
    
    def set_r_bins(self, r_bins):
        self.r_bins = r_bins
        
    def set_th_bins(self, th_bins):
        self.th_bins = th_bins
        
    def set_phi_bins(self, phi_bins):
        self.phi_bins = phi_bins
    
    def attr_dict(self):
        
        attributes = {k: self.__dict__[k] for k in self.__dict__.keys() 
                      - {
                          "r", "th", "phi",
                          "neighbours", "r_bins", "th_bins", "phi_bins", 
                          "neighbours_bins"
                      }
                     }
        
        return attributes
    
    def initialize(self):
        
        self.B_mse_sph = [np.array([np.nan]), np.array([np.nan]), np.array([np.nan])]

    def average(self, A):
        warnings.filterwarnings(action='ignore', message='Mean of empty slice')
        A_average = [np.nanmean(comp) for comp in A]
        
        return A_average

    def sigma(self, A):
        warnings.filterwarnings(action='ignore', message='Mean of empty slice')
        if len(A) >1:
            sigma = np.sqrt(np.nansum((A-np.nanmean(A))**2, axis = 0)/(len(A)*(len(A)-1)))
        else:
            sigma=np.nan
        return sigma
    
    def B_average(self):
        
        self.B_mse_mean = self.average(self.B_mse_sph)
        self.sigma_Br = self.sigma(self.B_mse_sph[0])
        self.sigma_Bth = self.sigma(self.B_mse_sph[1])
        self.sigma_Bphi = self.sigma(self.B_mse_sph[2])
    
    def sph_to_cart(self, r, th, phi):
        
        """ Meant to be called as method for a Cell 'object'. It calls 
            the grid_cell_geometry sph_to_cart function. """
        
        x, y, z = gcm.sph_to_cart(r, th, phi)

        return [x, y, z]
    
    def cart_to_sph(self, x, y, z):
        
        """ Meant to be called as method for a Cell 'object'. It calls 
            the grid_cell_geometry cart_to_sph function. """
        
        r, theta, phi = gcm.cart_to_sph(x, y, z)

        return [r, theta, phi]
    
    def set_neighbours_bins(self):
        
        coord_bins = ['r_bin', 'th_bin', 'phi_bin']
        
        neighbours_bins = {'r':{-1:{}, +1:{}}, 
                          'th':{-1:{}, +1:{}}, 
                         'phi':{-1:{}, +1:{}}}
        
        for ic, coordinate in enumerate(neighbours_bins.keys()):
            
            ic_other = [i for i in range(3) if i != ic]
            
            for direction in neighbours_bins[coordinate].keys():
                
                neighbours_bins[coordinate][direction] = dict.fromkeys(coord_bins)
                    
                neighbours_bins[coordinate][direction][coordinate + '_bin'] = getattr(self, coordinate + '_bin') + direction
                    
                for ic in ic_other:
                    
                    other_coord_bins = coord_bins[ic]

                    neighbours_bins[coordinate][direction][other_coord_bins] = getattr(self, other_coord_bins)

                if coordinate == 'r' and ((self.r_bin == self.r_bins.max() and direction == +1) or (self.r_bin == self.r_bins.min() and direction == -1)):
                    
                    for coord_bin in coord_bins:
                        
                        neighbours_bins[coordinate][direction][coord_bin] = np.nan

                if coordinate == 'th' and ((self.th_bin == self.th_bins.max() and direction == +1) or (self.th_bin == self.th_bins.min() and direction == -1)):

                    for coord_bin in coord_bins:
                        
                        neighbours_bins[coordinate][direction][coord_bin] = np.nan

                if coordinate == 'phi' and self.phi_bin == self.phi_bins.max() and direction == +1:

                    neighbours_bins[coordinate][direction][coordinate + '_bin'] = self.phi_bins.min()

                elif coordinate == 'phi' and self.phi_bin == self.phi_bins.min() and direction == -1:

                    neighbours_bins[coordinate][direction][coordinate + '_bin'] = self.phi_bins.max()

        self.neighbours_bins = neighbours_bins
    
    def set_neighbour(self, coordinate, direction, neighbour):
        
        self.neighbours[coordinate][direction] = neighbour 
        
    def neighbours_idx(self):
        
        """ Find the indices of coordinates for the cell's neighbours, by just going one index up or down for each coordinate
            keeping the other two constant. Each cell should have 6 neighbours, except for those that are closest to the poles 
            and those in the inner and outer layers. """
        
        r_idx_neighb = [self.r_idx-1, self.r_idx+1] + 4*[self.r_idx]
        th_idx_neighb = 2*[self.th_idx] + [self.th_idx-1, self.th_idx+1] + 2*[self.th_idx]
        phi_idx_neighb = 4*[self.phi_idx] + [self.phi_idx-1, self.phi_idx+1]
        
        if self.phi_idx == 0:
            phi_idx_neighb[-2] = -1
        elif self.phi_idx + 1 == len(self.phi):
            phi_idx_neighb[-1] = 0

        
        if self.r_idx == 0 or self.r_idx + 1 == len(self.r):
            r_idx_neighb.pop(np.where(self.r_idx == 0, 0, 1))
            th_idx_neighb.pop(np.where(self.r_idx == 0, 0, 1))
            phi_idx_neighb.pop(np.where(self.r_idx == 0, 0, 1))
            
            if self.th_idx == 0 or self.th_idx + 1 == len(self.th):
                r_idx_neighb.pop(np.where(self.th_idx == 0, 1, 2))
                th_idx_neighb.pop(np.where(self.th_idx == 0, 1, 2))
                phi_idx_neighb.pop(np.where(self.th_idx == 0, 1, 2))
        
        elif self.th_idx == 0 or self.th_idx + 1 == len(self.th):
            r_idx_neighb.pop(np.where(self.th_idx == 0, 2, 3))
            th_idx_neighb.pop(np.where(self.th_idx == 0, 2, 3))
            phi_idx_neighb.pop(np.where(self.th_idx == 0, 2, 3))
            
        neighbours = []
        
        for r_idx, th_idx, phi_idx in zip(r_idx_neighb, th_idx_neighb, phi_idx_neighb):
            neighbours.append([r_idx, th_idx, phi_idx])
            
        return neighbours

    def neighbours_coord_cart(self):
        
        """ Taking the indices of coordinates of the neighbours, returning the actual coordinates, in cartesian and spherical coordinates,
            as well as the cell's centers (will probably remove this later, not really useful). """
        
        neigh = self.neighbours_idx()
        r_neigh  = [self.r[neigh[i][0]] for i in range(len(neigh))]
        th_neigh = [self.th[neigh[j][1]] for j in range(len(neigh))]
        phi_neigh = [self.phi[neigh[k][2]] for k in range(len(neigh))]

        neigh_pos_cart = [gcm.sph_to_cart(r_neigh[i], th_neigh[i], phi_neigh[i]) for i in range(len(neigh))]
       
        return neigh_pos_cart

    def vertices_coord(self, r_c, th_c, phi_c):
        
        """ Returns the spherical coordinates of vertices, for cell centered at (r_c, th_c, phi_c). 
            The bertices coordinates are calculated by adding or substracting dr/2, dth/2, dphi/2 from 
            the cell's central coordinates. """
        
        # This if is useless right now, only 'else' is ever executed. 
        # It would only go to 'if' if theta is ever 0 and/or pi,
        # but should be fixed. The shape of the cells at the poles is problematic.
        
#         if th_c == 0 or th_c == 180:
#             if th_c == 0: sgn = +1
#             if th_c == np.pi: sgn = -1
#             th_vert = abs(th_c + sgn*self.dth/2)
#             zero = [r_c + self.dr/2, th_c + th_vert, 225]
#             one = [r_c + self.dr/2, th_c + th_vert, 135]
#             two = [r_c + self.dr/2, th_c + th_vert, 45]
#             three = [r_c + self.dr/2, th_c + th_vert,  315]
#             four = [r_c - self.dr/2, th_c + th_vert, 315]
#             five = [r_c - self.dr/2, th_c + th_vert, 45]
#             six = [r_c - self.dr/2, th_c + th_vert, 135]
#             seven = [r_c - self.dr/2, th_c + fth_vert, 225]
            
#         else:
                
        zero = [r_c + self.dr/2, th_c - self.dth/2, phi_c + self.dphi/2]
        one = [r_c + self.dr/2, th_c + self.dth/2, phi_c + self.dphi/2]
        two = [r_c + self.dr/2, th_c + self.dth/2, phi_c - self.dphi/2]
        three = [r_c + self.dr/2, th_c - self.dth/2, phi_c - self.dphi/2]
        four = [r_c - self.dr/2, th_c - self.dth/2, phi_c - self.dphi/2]
        five = [r_c - self.dr/2, th_c + self.dth/2, phi_c - self.dphi/2]
        six = [r_c - self.dr/2, th_c + self.dth/2, phi_c + self.dphi/2]
        seven = [r_c - self.dr/2, th_c - self.dth/2, phi_c + self.dphi/2]

        return [zero, one, two, three, four, five, six, seven]

    def vertices_coord_cart(self, r_c, th_c, phi_c):
        
        """ Transform spherical coordinates of cell vertices to cartesian. """
        
        vertices_coord_sph = self.vertices_coord(r_c, th_c, phi_c)
        to_cartesian = [gcm.sph_to_cart(r, th, phi) for r, th, phi in vertices_coord_sph]
        
        return to_cartesian


    def cell_side_arc(self, vertices, num):
        
        """ Returns the circle arcs (r = const.), which are sides of the cell.
            It gets the two vertices of the side as inputs and the number of points of the arc to be calculated.
            It rotates the two vertices onto the xy-plane. The rotation axis is found by calculating the plane defined by the
            vertices and the origin, then take make a new orthogonal system with the normal to the tilted plane vector, the 
            vector from the origin to one of the vertices and finally the rotation axis completes the system.
            Then, the vertices are rotated on the xy-plane, the arc between them is calculated and then rotated back to the 
            tilted plane. The arc coordinates are returned in cartesian coordinates. """
        
        th_lim = [min(vertices[0][1], vertices[1][1]), max(vertices[0][1], vertices[1][1])]
        phi_lim = [min(vertices[0][2], vertices[1][2]), max(vertices[0][2], vertices[1][2])]
        
        vertices_cart = [ gcm.sph_to_cart(*vertices[0]), gcm.sph_to_cart(*vertices[1]) ]
        vertices_xy = gcm.rotate_to_xy(*vertices_cart)
        arc_xy = gcm.arc_on_xy(vertices_xy, num)
        rot_ax, angle = gcm.rot_axis_angle(*vertices_cart)

        arc_side = np.dot(gcm.rot_mat(rot_ax, -angle), arc_xy)
        
        return arc_side
        
    def cell_side(self, vertices, num):
        
        """ Spherical coordinates of vertices of side and number of points on the side to be calculated as inputs. 
            If the radius of the two vertices is constant, the side is an arc (calls cell_side_arc()). If theta=const. or
            phi=const. for the two vertices it calculates the straight line connecting them. """
        
        if vertices[0][0] == vertices[1][0]:
            # Circle arc side (for r=const.)
            x_side, y_side, z_side = self.cell_side_arc(vertices, num)
            
        else:
            
            #Straight line side (for theta=conts., phi=const.)
            vert0, vert1 = [gcm.sph_to_cart(r, th, phi) for r, th, phi in vertices]
            
            x_side, y_side, z_side = [np.linspace(vert0[i], vert1[i], num) for i in range(len(vert0))]
            
        return [x_side, y_side, z_side]
    
    def plot_cell(self, fig, num, color_faces = True, plot_neighbours = True):
        
        """ Function to be called from outside the class, to plot the cell. Needs plotly fig as input, number of points to be calculated
            on each cell side. If color_faces==True, the faces are colored. If plot_neighbours==True the neighbouring cells are also plotted. """
        
        vertices_sph = self.vertices_coord(self.r_c, self.th_c, self.phi_c)
        
        # Vertex pairs, each pair represents a side
        vertices_pairs = [ [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 3], [0, 7], [1, 6], [2, 5], [4, 7] ]
        
        # Faces, each face is defines by 4 sides
        faces = {'r_R': [0, 1, 2, 7], 'r_L': [4, 5, 6, 11], 
                 'th_R': [1, 5, 9, 10], 'th_L': [3, 7, 8, 11], 
                 'phi_R': [0, 8, 6, 9], 'phi_L': [2, 3, 4, 10]}
        
        vert0 = [verts[0] for verts in vertices_pairs]
        vert1 = [verts[1] for verts in vertices_pairs]

        sides = [self.cell_side([vertices_sph[i], vertices_sph[j]], num) for i, j in zip(vert0, vert1)]
        
        for side in sides:
            
            side = list(side)
            color = 'red' if plot_neighbours else 'black'
            line_width = 8 if plot_neighbours else 4
            fig.add_trace(go.Scatter3d(x=side[0], y=side[1], z=side[2], mode='lines', line=go.scatter3d.Line(color=color, width=line_width)))
        
        if color_faces:
            
            for face in faces:
                
                face_sides = faces.get(face)
                face_x = np.hstack([x for x in (sides[i][0] for i in face_sides)]).flatten()
                face_y = np.hstack([x for x in (sides[i][1] for i in face_sides)]).flatten()
                face_z = np.hstack([x for x in (sides[i][2] for i in face_sides)]).flatten()
                    
                points2D=np.vstack([face_x,face_y]).T
                tri=Delaunay(points2D, qhull_options="QJ Pp")
                
                surface = gcm.plotly_trisurf(face_x,face_y,face_z, tri.simplices, plot_edges=None)
                fig.add_trace(surface[0])
        
        
        if plot_neighbours:
            
            n_cart = self.neighbours_coord_cart()
            
            for neighbour in n_cart:
                neighbour = self.cart_to_sph(*neighbour)
                vertices_sph = self.vertices_coord(*neighbour)
                sides = [self.cell_side([vertices_sph[i], vertices_sph[j]], num) for i, j in zip(vert0, vert1)]
                
                for side in sides:
                    side = list(side)
                    fig.add_trace(go.Scatter3d(x=side[0], y=side[1], z=side[2], mode='lines', line=go.scatter3d.Line(color="black", width=4)))
        
                if color_faces:
            
                    for face in faces:
                
                        face_sides = faces.get(face)
                        face_x = np.hstack([x for x in (sides[i][0] for i in face_sides)]).flatten()
                        face_y = np.hstack([x for x in (sides[i][1] for i in face_sides)]).flatten()
                        face_z = np.hstack([x for x in (sides[i][2] for i in face_sides)]).flatten()

                        points2D=np.vstack([face_x,face_y]).T
                        tri=Delaunay(points2D, qhull_options="QJ Pp")

                        surface = gcm.plotly_trisurf(face_x,face_y,face_z, tri.simplices, face_color = 'red', opacity = 0.05, plot_edges=None)
                        fig.add_trace(surface[0])
                        
        fig.add_trace(go.Scatter3d(x=np.array(0),y=np.array(0),z=np.array(0), mode='markers', marker=dict(size=2, color='blue')))
        
        return 
