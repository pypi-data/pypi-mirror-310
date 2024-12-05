from .generic.cart_to_sph_vf import cart_to_sph_vf
from .generic.sph_to_cart_vf import sph_to_cart_vf
from .grid import load_grid
import pandas as pd
import numpy as np
# import pickle
# import sys
import scipy
# import os
import spiceypy as spice
import astropy.convolution

def load_pck_kernel(pck_file):
    
    return spice.furnsh(pck_file)

def smoothing_3d(B, kernel, mode="nearest"):
        
    B_smoothed = scipy.ndimage.convolve(B, kernel, mode=mode)
    nans_positions = np.where(np.isnan(B_smoothed))
    
    # B_smoothed[nans_positions] = B[nans_positions] if np.isnan(B[nans_positions]) == False else B_smoothed[nans_positions]
    if nans_positions[0].size > 0:
        B_smoothed[nans_positions] = np.where(
            np.isnan(B[nans_positions]) == False,
            B[nans_positions],
            B_smoothed[nans_positions],
        )
    return B_smoothed
    
def init_grid(data_file_name=None, load_from_file=False, file_path=None, dr=None, dth=None, dphi=None, r_lim=None, th_lim=None, phi_lim=None):

    if data_file_name is not None and load_from_file==False:

        grid_dict = dict(dr = dr, dth_deg = dth, dphi_deg = dphi, r_lim = r_lim, th_lim_deg = th_lim
                 , phi_lim_deg = phi_lim)
    
        grid = load_grid(grid_dict, load_from_file = load_from_file, data = data_file_name)
        
    elif file_path is not None and load_from_file:

        grid = load_grid(load_from_file = load_from_file, 
                                file_path = file_path)

    return grid

def binning(grid, data_file_name=None):#, pck_file=None):

    r = grid.r
    th = grid.th
    phi = grid.phi

    if data_file_name is None:

        print('No data file given \n')
        
        return
        
    elif data_file_name is not None:

        """Read the mag_mse file into a pandas dataframe"""
    
        df = pd.read_csv(data_file_name)
        df = df.drop(df[np.isnan(df["R_mse"])].index)
        df = df[['Bx_mse','By_mse','Bz_mse','X_mse','Y_mse','Z_mse','R_mse','th_mse','phi_mse']]

        r_binned = np.digitize(df["R_mse"].values, grid.r_bins, right=True)
        th_binned = np.digitize(df["th_mse"].values, grid.th_bins, right=True)
        phi_binned = np.digitize(df["phi_mse"].values, grid.phi_bins, right=True)
    
        B_mse_cart = [
            [Bx, By, Bz] for Bx, By, Bz in zip(df["Bx_mse"], df["By_mse"], df["Bz_mse"])
        ]
        B_mse_sph = cart_to_sph_vf(B_mse_cart, df["th_mse"].values, df["phi_mse"].values)
        
        df["Br_mse"] = [B_sph.A[0][0] for B_sph in B_mse_sph]
        df["Bth_mse"] = [B_sph.A[0][1] for B_sph in B_mse_sph]
        df["Bphi_mse"] = [B_sph.A[0][2] for B_sph in B_mse_sph]
    
        df["r_bin"] = r_binned
        df["th_bin"] = th_binned
        df["phi_bin"] = phi_binned

        df = df.drop(columns=["Bx_mse", "By_mse", "Bz_mse", "X_mse", "Y_mse", "Z_mse"], axis=1)

        """Binning, by comparing the r,th,phi bins of each data point with the ones from the cells. Then average to get B_mse_mean in spherical
       cooridnates, and get cartesian cooridnates and magentic field components of the cells, to plot the 3D cone plot. Might also be used
       to make slice plots."""

        grid.X_cells = []
        grid.Y_cells = []
        grid.Z_cells = []
        grid.Bx_cells = []
        grid.By_cells = []
        grid.Bz_cells = []
        
        for cell in grid.cells:
            
            cell.initialize()
            df_data_in_bin = df.loc[
                (df["r_bin"] == cell.r_bin)
                & (df["th_bin"] == cell.th_bin)
                & (df["phi_bin"] == cell.phi_bin),
                ["Br_mse", "Bth_mse", "Bphi_mse"],
            ]  #'R_mse', 'th_mse', 'phi_mse',
    
            if not df_data_in_bin.empty:
    
                cell.B_mse_sph[0] = df_data_in_bin["Br_mse"].values
                cell.B_mse_sph[1] = df_data_in_bin["Bth_mse"].values
                cell.B_mse_sph[2] = df_data_in_bin["Bphi_mse"].values
    
                del df_data_in_bin
    
                cell.n_measurements = len(cell.B_mse_sph[0])
            else:
                cell.n_measurements = np.nan
    
            cell.B_average()
            cell.X, cell.Y, cell.Z = cell.sph_to_cart(cell.r_c, cell.th_c, cell.phi_c)
            cell.Bx, cell.By, cell.Bz = sph_to_cart_vf(
                cell.B_mse_mean, cell.th_c, cell.phi_c
            ).A.tolist()[0]
    
            grid.X_cells.append(cell.X)
            grid.Y_cells.append(cell.Y)
            grid.Z_cells.append(cell.Z)
        
            grid.Bx_cells.append(cell.Bx)
            grid.By_cells.append(cell.By)
            grid.Bz_cells.append(cell.Bz)
            
        del df

        grid.Br = np.empty((len(phi), len(th), len(r)))
        grid.Br[:] = np.nan
        grid.Bth = np.empty((len(phi), len(th), len(r)))
        grid.Bth[:] = np.nan
        grid.Bphi = np.empty((len(phi), len(th), len(r)))
        grid.Bphi[:] = np.nan
        grid.sigma_Br = np.empty((len(phi), len(th), len(r)))
        grid.sigma_Br[:] = np.nan
        grid.sigma_Bth = np.empty((len(phi), len(th), len(r)))
        grid.sigma_Bth[:] = np.nan
        grid.sigma_Bphi = np.empty((len(phi), len(th), len(r)))
        grid.sigma_Bphi[:] = np.nan

        grid.th_2d = np.empty((len(phi), len(th), len(r)))
        grid.th_2d[:] = np.nan
        grid.phi_2d = np.empty((len(phi), len(th), len(r)))
        grid.phi_2d[:] = np.nan
        grid.measurement_counts = np.empty((len(phi), len(th), len(r)))
    
        for i in range(grid.Br.shape[0]):
            for j in range(grid.Br.shape[1]):
                for k in range(grid.Br.shape[2]):
                    matching_cell = []
                    for cell in grid.cells:
                        if (
                            cell.r_bin == k + 1
                            and cell.th_bin == j + 1
                            and cell.phi_bin == i + 1
                        ):
                            matching_cell.append(cell)
                            break
    
                    if not bool(matching_cell):
    
                        grid.Br[i, j, k] = np.nan
                        grid.Bth[i, j, k] = np.nan
                        grid.Bphi[i, j, k] = np.nan
                        grid.sigma_Br[i,j,k] = np.nan
                        grid.sigma_Bth[i,j,k] = np.nan
                        grid.sigma_Bphi[i,j,k] = np.nan
                        grid.th_2d[i, j, k] = th[j]
                        grid.phi_2d[i, j, k] = phi[i]
                        grid.measurement_counts[i, j, k] = np.nan
    
                    elif len(matching_cell) == 1:
    
                        grid.Br[i, j, k] = matching_cell[0].B_mse_mean[0]
                        grid.Bth[i, j, k] = matching_cell[0].B_mse_mean[1]
                        grid.Bphi[i, j, k] = matching_cell[0].B_mse_mean[2]
                        grid.sigma_Br[i,j,k] = matching_cell[0].sigma_Br
                        grid.sigma_Bth[i,j,k] = matching_cell[0].sigma_Bth
                        grid.sigma_Bphi[i,j,k] = matching_cell[0].sigma_Bphi
                        grid.th_2d[i, j, k] = matching_cell[0].th_c
                        grid.phi_2d[i, j, k] = matching_cell[0].phi_c
                        grid.measurement_counts[i, j, k] = matching_cell[0].n_measurements
    
                    else:
                        print("Grid error")

        """Kernel for use as an average filter, across the image. Takes into account central cell and the 6 cells that share faces with it."""

        kernel = (
            1
            / 7
            * 
            np.array(
                [
                    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
                    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                ]
            )
        )

        """Function that performs smoothing, convoluting the kernel above with the component 3D images. On the image edges the "nearest" 
        neighbours are used. NaNs are propagating when used on the convolution. After the filtering, the new NaNs are replace with 
       their old, unsmoothed values."""
        
        grid.Br_sm = astropy.convolution.convolve(grid.Br, kernel, boundary ='extend', nan_treatment='interpolate', normalize_kernel = True,  preserve_nan = True)
        grid.Bth_sm = astropy.convolution.convolve(grid.Bth, kernel, boundary ='extend', nan_treatment='interpolate', normalize_kernel = True,  preserve_nan = True)
        grid.Bphi_sm = astropy.convolution.convolve(grid.Bphi, kernel, boundary ='extend', nan_treatment='interpolate', normalize_kernel = True,  preserve_nan = True)

        for i in range(grid.Br_sm.shape[0]):
            for j in range(grid.Br_sm.shape[1]):
                for k in range(grid.Br_sm.shape[2]):
                    count = 0
                    for cell in grid.cells:
        
                        if (
                            cell.r_bin == k + 1
                            and cell.th_bin == j + 1
                            and cell.phi_bin == i + 1
                        ):
                            count += 1
                            cell.Br = grid.Br_sm[i, j, k]
                            cell.Bth = grid.Bth_sm[i, j, k]
                            cell.Bphi = grid.Bphi_sm[i, j, k]
        
                            break
        
                    if count == 0 or count > 1:
                        print("Grid error")
    return grid