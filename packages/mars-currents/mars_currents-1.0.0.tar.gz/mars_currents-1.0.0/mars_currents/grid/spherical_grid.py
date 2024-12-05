# from ..generic.cart_to_sph_vf import cart_to_sph_vf
# from ..generic.sph_to_cart_vf import sph_to_cart_vf
# import os
import numpy as np
from .cell import Cell
from .curl import curl
from .div import div 
from .sigma_gradient import sigma_gradient
import re
import pickle 

class Grid:

    def __init__(self, grid_dict, load_from_file = False, file_path = None, data = None, grid_name = None):
        
        for attr in grid_dict.keys() - {"cells", "r_bins", "th_bins", "phi_bins", "r", "th", "phi", "cells_dict"}:
                    
            self.__setattr__(attr, grid_dict[attr])
                    
        self.data = data if "data" not in grid_dict.keys() else grid_dict["data"]
        self.grid_name = grid_name if "grid_name" not in grid_dict.keys() else grid_dict['grid_name']
        self.load_from_file = load_from_file 

        th_lim = np.deg2rad(self.th_lim_deg)
        phi_lim = np.deg2rad(self.phi_lim_deg)

        self.dth = np.deg2rad(self.dth_deg)
        self.dphi = np.deg2rad(self.dphi_deg)

        if self.load_from_file == False:
            
            (
                self.cells,
                self.r_bins,
                self.th_bins,
                self.phi_bins,
                self.r,
                self.th,
                self.phi,
            ) = self._set_grid_cells(self.r_lim, th_lim, phi_lim, self.dr, self.dth, self.dphi)
            
        else:
                    
            self.r_bins = grid_dict["r_bins"]
            self.th_bins = grid_dict["th_bins"]
            self.phi_bins = grid_dict["phi_bins"]
            self.r = grid_dict["r"]
            self.th = grid_dict["th"]
            self.phi = grid_dict["phi"]
            self.cells_dict = grid_dict["cells_dict"]
            
            self.cells = self._set_grid_cells(cells_dict = self.cells_dict)
                

    def _set_grid_cells(
        self, r_lim=None, th_lim=None, phi_lim=None, dr=None, dth=None, dphi=None,
        cells_dict = None):

        # th_lim = np.deg2rad(th_lim); phi_lim = np.deg2rad(phi_lim)
        # dth = np.deg2rad(dth); dphi = np.deg2rad(dphi)
        if self.load_from_file:

            cells = []

            for _, cell_dict in cells_dict.items():
                
                cell = Cell(cell_dict['dr'], cell_dict['dth'], cell_dict['dphi'], cell_dict['r_idx'], 
                            cell_dict['th_idx'], cell_dict['phi_idx'], self.r, self.th, self.phi)
                
                for attr in cell_dict.keys():
                    
                    cell.__setattr__(attr, cell_dict[attr])
#                 cell.set_r_bin(cell_dict['r_bin'])
#                 cell.set_th_bin(cell_dict['th_bin'])
#                 cell.set_phi_bin(cell_dict['phi_bin'])

#                 cell.neighbours = cell_dict["neighbours"]
                
                cells.append(cell)
                
            return cells
            
        else:

            r = np.arange(r_lim[0], r_lim[1] + dr, dr)
            th = np.arange(th_lim[0] + dth/2 , th_lim[1]+dth/2, dth)
            phi = np.arange(phi_lim[0] + dphi/2 , phi_lim[1] + dphi/2, dphi)
            
            # phi = np.arange(phi_lim[0], phi_lim[1]-dphi/2, dphi)
            
            r_bins = np.array(
                [
                    r[0] + (2 * n - 1) * dr / 2
                    for n in range(len(r))
                    if (r[0] + (n - 1) * dr) <= r[-1]
                ]
            )
            th_bins = np.array(
                [
                    th[0] + (2 * n - 1) * dth / 2
                    for n in range(len(th))
                    if (th[0] + (n - 1) * dth) <= th[-1]
                ]
            )
            phi_bins = np.array(
                [
                    phi[0] + (2 * n - 1) * dphi / 2
                    for n in range(len(phi))
                    if (phi[0] + (n - 1) * dphi) <= phi[-1]
                ]
            )

            cells = []

            for i in range(len(r)):

                r_shell = np.digitize(r[i], r_bins, right=True)

                for j in range(len(th)):

                    th_shell = np.digitize(th[j], th_bins, right=True)

                    for k in range(len(phi)):

                        cell = Cell(dr, dth, dphi, i, j, k, r, th, phi)
                        # cell.B_mse_sph = [[], [], []]
                        # cell.P_mse_sph = [[], [], []]
                        cells.append(cell)
                        phi_shell = np.digitize(phi[k], phi_bins, right=True)

                        cell.set_r_bins(np.digitize(r, r_bins, right=True))
                        cell.set_th_bins(np.digitize(th, th_bins, right=True))
                        cell.set_phi_bins(np.digitize(phi, phi_bins, right=True))

                        cell.set_r_bin(r_shell)
                        cell.set_th_bin(th_shell)
                        cell.set_phi_bin(phi_shell)
                        cell.set_neighbours_bins()

            for cell in cells:

                for coordinate in ["r", "th", "phi"]:

                    for direction in [-1, +1]:
                        neighbour = None
                        for c in cells:

                            if (
                                cell.neighbours_bins[coordinate][direction]["r_bin"]
                                == c.r_bin
                                and cell.neighbours_bins[coordinate][direction]["th_bin"]
                                == c.th_bin
                                and cell.neighbours_bins[coordinate][direction]["phi_bin"]
                                == c.phi_bin
                            ):

                                neighbour = c
                                break
                        cell.set_neighbour(coordinate, direction, neighbour)
            
            
            return cells, r_bins, th_bins, phi_bins, r, th, phi

    def current_densities(self, radius):
        
        mu0 = 1.25663706212e-6
        
        if self.load_from_file:
            
            for cell in self.cells:
                
                curlB = np.array(curl(cell.attr_dict(), cell.neighbours, field = 'B'))
                J = 1/(radius*1e3) * 1/(mu0) * curlB
                
                
                cell.divB_curlB = abs(div(cell.attr_dict(), cell.neighbours, field = "B")) / np.linalg.norm(curlB)
                
                cell.Jr, cell.Jth, cell.Jphi = J[0], J[1], J[2]

            for cell in self.cells:
                cell.divJ_magJ = abs(div(cell.attr_dict(), cell.neighbours, field = "J")) / np.sqrt(cell.Jr**2+cell.Jth**2+cell.Jphi**2)
                
                cell.sigma_Jr = 1/mu0 * np.sqrt((1/(cell.r_c*radius*1e3) * sigma_gradient(cell.attr_dict(), cell.neighbours, "B", "phi", "th"))**2 + (np.cos(cell.th_c)/(cell.r_c*radius*1e3*np.sin(cell.th_c)) * cell.sigma_Bphi)**2 + (1/(cell.r_c*radius*1e3*np.sin(cell.th_c))*sigma_gradient(cell.attr_dict(), cell.neighbours, "B", "th", "phi"))**2)#/abs(cell.Jr)
                
                cell.sigma_Jth = 1/mu0 * np.sqrt((1/(cell.r_c*radius *1e3 * np.sin(cell.th_c)) * sigma_gradient(cell.attr_dict(), cell.neighbours, "B", "r", "phi"))**2 + (sigma_gradient(cell.attr_dict(), cell.neighbours, "B", "phi", "r")/(radius*1e3))**2 + (1/(cell.r_c*radius*1e3) * cell.sigma_Bphi)**2) #/ abs(cell.Jth)
                
                cell.sigma_Jphi = 1/mu0 * np.sqrt((sigma_gradient(cell.attr_dict(), cell.neighbours, "B", "th", "r")/(radius*1e3))**2 + (1/(cell.r_c*radius*1e3) * cell.sigma_Bth)**2 + (1/(cell.r_c*radius*1e3) * sigma_gradient(cell.attr_dict(), cell.neighbours, "B", "r", "th"))**2)# / abs(cell.Jphi)
                
                
        else:
            
            for cell in self.cells:
                
                neighbours_dict = {}
                
                for coordinate in cell.neighbours.keys():
                    
                    neighbours_dict[coordinate] = {}
                    
                    for direction in cell.neighbours[coordinate].keys():
                        
                        if cell.neighbours[coordinate][direction] == None:
                            
                            neighbour_dict = cell.attr_dict()
                            
                        else:

                            neighbour_dict = {k: cell.neighbours[coordinate][direction].__dict__[k]
                                             for k in cell.neighbours[coordinate][direction].__dict__.keys()
                                             - {
                                                  "r", "th", "phi",
                                                  "neighbours", "r_bins", "th_bins", "phi_bins", 
                                                  "neighbours_bins"
                                             }}
                        
                        neighbours_dict[coordinate].update({direction: neighbour_dict})
                
                curlB = np.array(curl(cell.attr_dict(), neighbours_dict, field = 'B'))
                J = 1/(radius*1e3) * 1/(mu0) * curlB
                
                cell.divB_curlB = abs(div(cell.attr_dict(), neighbours_dict, field = "B")) / np.linalg.norm(curlB)
                
                cell.Jr, cell.Jth, cell.Jphi = J[0], J[1], J[2]
                
            for cell in self.cells:
                neighbours_dict = {}
                
                for coordinate in cell.neighbours.keys():
                    
                    neighbours_dict[coordinate] = {}
                    
                    for direction in cell.neighbours[coordinate].keys():
                        
                        if cell.neighbours[coordinate][direction] == None:
                            
                            neighbour_dict = cell.attr_dict()
                            
                        else:

                            neighbour_dict = {k: cell.neighbours[coordinate][direction].__dict__[k]
                                             for k in cell.neighbours[coordinate][direction].__dict__.keys()
                                             - {
                                                  "r", "th", "phi",
                                                  "neighbours", "r_bins", "th_bins", "phi_bins", 
                                                  "neighbours_bins"
                                             }}
                        
                        neighbours_dict[coordinate].update({direction: neighbour_dict})
                cell.divJ_magJ = abs(div(cell.attr_dict(), neighbours_dict, field = "J")) / np.sqrt(cell.Jr**2+cell.Jth**2+cell.Jphi**2) #/(radius*1e3)
                
                cell.sigma_Jr = 1/mu0 * np.sqrt((1/(cell.r_c*radius*1e3) * sigma_gradient(cell.attr_dict(), neighbours_dict, "B", "phi", "th"))**2 + (np.cos(cell.th_c)/(cell.r_c*radius*1e3*np.sin(cell.th_c)) * cell.sigma_Bphi)**2 + (1/(cell.r_c*radius*1e3*np.sin(cell.th_c))*sigma_gradient(cell.attr_dict(), neighbours_dict, "B", "th", "phi"))**2)#/abs(cell.Jr)

                cell.sigma_Jth = 1/mu0 * np.sqrt((1/(cell.r_c * radius*1e3 *np.sin(cell.th_c)) * sigma_gradient(cell.attr_dict(), neighbours_dict, "B", "r", "phi"))**2 + (sigma_gradient(cell.attr_dict(), neighbours_dict, "B", "phi", "r")/(radius*1e3))**2 + (1/(cell.r_c*radius*1e3) * cell.sigma_Bphi)**2) #/ abs(cell.Jth)
                
                cell.sigma_Jphi = 1/mu0 * np.sqrt((sigma_gradient(cell.attr_dict(), neighbours_dict, "B", "th", "r")/(radius*1e3))**2 + (1/(cell.r_c*radius*1e3) * cell.sigma_Bth)**2 + (1/(cell.r_c*radius*1e3) * sigma_gradient(cell.attr_dict(), neighbours_dict, "B", "r", "th"))**2) #/ abs(cell.Jphi)
                
    def grid_to_dict(self):

        grid_dict = self.__dict__
        
        if not self.load_from_file:
            save_dict = {k: grid_dict[k] for k in grid_dict.keys() - {"cells", "save_dict"}}
        else:
            save_dict = {k: grid_dict[k] for k in grid_dict.keys() - {"save_dict"}}
            
        save_dict["cells_dict"] = {}
        c = 0

        for cell in self.cells:

            cell_dict = cell.__dict__
            cell_save_dict = {
                k: cell_dict[k]
                for k in cell_dict.keys()
                - {
                    "r",
                    "th", "phi",
                    "neighbours",
                    "r_bins",
                    "th_bins",
                    "phi_bins",
                    "neighbours_bins",
                }
            }

            save_dict["cells_dict"].update({c: cell_save_dict})

            neighbours = {}
            for coordinate in cell_dict["neighbours"].keys():
                neighbours[coordinate] = {}
                for direction in cell_dict["neighbours"][coordinate].keys():
                    
                    if cell_dict['neighbours'][coordinate][direction] is not None:
                        
                        if isinstance(cell_dict["neighbours"][coordinate][direction], dict):
                            neighbour_dict = cell_dict["neighbours"][coordinate][direction]
                            
                        else: 
                            neighbour_dict = cell_dict["neighbours"][coordinate][direction].__dict__
                            
                        neighbours[coordinate].update(
                            {
                                direction: {
                                    k: neighbour_dict[k]
                                    for k in neighbour_dict.keys()
                                    - {
                                        "r",
                                        "th", "phi",
                                        "neighbours",
                                        "r_bins",
                                        "th_bins",
                                        "phi_bins",
                                        "neighbours_bins",
                                        "r_bin",
                                        "th_bin",
                                        "phi_bin"
                                    }
                                }
                            }
                        )
                    else:
                        
                        neighbours[coordinate].update({direction: None})

            save_dict["cells_dict"][c]["neighbours"] = neighbours
            c+=1

        self.save_dict = save_dict

    def currents_uncertainties(self, radius):

        r = self.r; th = self.th; phi = self.phi
        self.current_densities(radius = radius)
    
        self.Jr = np.empty((len(phi), len(th), len(r)))
        self.Jr[:] = np.nan
        self.Jth = np.empty((len(phi), len(th), len(r)))
        self.Jth[:] = np.nan
        self.Jphi = np.empty((len(phi), len(th), len(r)))
        self.Jphi[:] = np.nan
        self.sigma_Jr = np.empty((len(phi), len(th), len(r)))
        self.sigma_Jr[:] = np.nan
        self.sigma_Jth = np.empty((len(phi), len(th), len(r)))
        self.sigma_Jth[:] = np.nan
        self.sigma_Jphi = np.empty((len(phi), len(th), len(r)))
        self.sigma_Jphi[:] = np.nan
        self.divJ_magJ = np.empty((len(phi), len(th), len(r)))
        self.divJ_magJ[:] = np.nan
        self.divB_curlB = np.empty((len(phi), len(th), len(r)))
        self.divB_curlB[:] = np.nan
    
        for i in range(self.Jr.shape[0]):
            for j in range(self.Jr.shape[1]):
                for k in range(self.Jr.shape[2]):
                    matching_cell = []
                    for cell in self.cells:
                        
                        if (
                            cell.r_bin == k + 1
                            and cell.th_bin == j + 1
                            and cell.phi_bin == i + 1
                        ):
                            matching_cell.append(cell)
                            break
    
                    if not bool(matching_cell):
    
                        self.Jr[i, j, k] = np.nan
                        self.Jth[i, j, k] = np.nan
                        self.Jphi[i, j, k] = np.nan
                        self.sigma_Jr[i,j,k] = np.nan
                        self.sigma_Jth[i,j,k] = np.nan
                        self.sigma_Jphi[i,j,k] = np.nan
                        self.divB_curlB[i, j, k] = np.nan
                        self.divJ_magJ[i, j,k ] = np.nan
                        
                    elif len(matching_cell) == 1:
    
                        self.Jr[i, j, k] = matching_cell[0].Jr
                        self.Jth[i, j, k] = matching_cell[0].Jth
                        self.Jphi[i, j, k] = matching_cell[0].Jphi
                        self.sigma_Jr[i,j,k] = matching_cell[0].sigma_Jr
                        self.sigma_Jth[i,j,k] = matching_cell[0].sigma_Jth
                        self.sigma_Jphi[i,j,k] = matching_cell[0].sigma_Jphi
                        self.divB_curlB[i, j, k] = matching_cell[0].divB_curlB
                        self.divJ_magJ[i, j, k ] = matching_cell[0].divJ_magJ
                        
                    else:
                        print("Grid error")
                        
        for cell in self.cells:
    
            cell.Ir = cell.Jr*cell.r_c**2*np.sin(cell.th_c)*cell.dth*cell.dphi *(radius* 1e3)**2 if not np.isnan(cell.Jr) else np.nan
            cell.Ith = cell.Jth*cell.r_c*np.sin(cell.th_c)*cell.dr*cell.dphi *(radius* 1e3)**2 if not np.isnan(cell.Jth) else np.nan
            cell.Iphi = cell.Jphi*cell.r_c*cell.dr*cell.dth *(radius* 1e3)**2 if not np.isnan(cell.Jphi) else np.nan
            
        for cell in self.cells:

            # if self.load_from_file:
                
            #     for attr in cell.neighboursattr_dict().keys():
                        
            #         self.__setattr__(attr, grid_dict[attr])
            
            cell.dI_I = np.nan
            
            dIr = 0
            
            if cell.neighbours['r'][+1] is not None:
                if not np.isnan(cell.neighbours['r'][+1].Jr):
                    dIr += cell.neighbours['r'][+1].Jr * (cell.neighbours['r'][+1].r_c)**2 * np.sin(cell.th_c) * cell.dth * cell.dphi * (radius* 1e3)**2
            else:
                dIr += cell.Ir
            if cell.neighbours['r'][-1] is not None:
                if not np.isnan(cell.neighbours['r'][-1].Jr):
                    dIr = dIr - cell.neighbours['r'][-1].Jr * (cell.neighbours['r'][-1].r_c)**2 * np.sin(cell.th_c) * cell.dth * cell.dphi * (radius* 1e3)**2
            else:
                dIr = dIr - cell.Ir
                
            dIth = 0
        
            if cell.neighbours['th'][+1] is not None:
                if not np.isnan(cell.neighbours['th'][+1].Jth):
                    dIth += cell.neighbours['th'][+1].Jth * cell.r_c*np.sin(cell.neighbours['th'][+1].th_c)*cell.dr*cell.dphi *(radius* 1e3)**2
            else:
                dIth += cell.Ith
            if cell.neighbours['th'][-1] is not None:
                if not np.isnan(cell.neighbours['th'][-1].Jth):
                    dIth = dIth - cell.neighbours['th'][-1].Jth * cell.r_c*np.sin(cell.neighbours['th'][-1].th_c)*cell.dr*cell.dphi *(radius* 1e3)**2
            else:
                dIth = dIth - cell.Ith
                
            dIphi = 0
        
            if cell.neighbours['phi'][+1] is not None:
                if not np.isnan(cell.neighbours['phi'][+1].Jphi):
                    dIphi += cell.neighbours['phi'][+1].Jphi * cell.r_c*cell.dr*cell.dth *(radius* 1e3)**2
            else:
                dIphi += cell.Iphi
            if cell.neighbours['phi'][-1] is not None:
                if not np.isnan(cell.neighbours['phi'][-1].Jphi):
                    dIphi = dIphi - cell.neighbours['phi'][-1].Jphi * cell.r_c*cell.dr*cell.dth *(radius* 1e3)**2
            else:
                dIphi = dIphi - cell.Iphi
            cell.dI_I = abs(dIr + dIth + dIphi)/np.sqrt(cell.Ir**2+cell.Ith**2+cell.Iphi**2)

        self.dI_I = np.empty((len(phi), len(th), len(r)))
        self.dI_I[:] = np.nan
        
        for i in range(self.dI_I.shape[0]):
            for j in range(self.dI_I.shape[1]):
                for k in range(self.dI_I.shape[2]):
                    matching_cell = []
                    for cell in self.cells:
                        
                        if (
                            cell.r_bin == k + 1
                            and cell.th_bin == j + 1
                            and cell.phi_bin == i + 1
                        ):
                            matching_cell.append(cell)
                            break
        
                    if not bool(matching_cell):
        
                        self.dI_I[i, j, k] = np.nan
                        
                    elif len(matching_cell) == 1:
        
                        self.dI_I[i, j, k] = matching_cell[0].dI_I
                        
                    else:
                        print("Grid error")

    def save_grid(self):

        with open(f"grid_{self.grid_name}__{re.sub('.csv','', re.sub(r'.*/' ,'', self.data))}.pickle", "wb") as f:
            self.grid_to_dict()
            pickle.dump(self.save_dict, f)