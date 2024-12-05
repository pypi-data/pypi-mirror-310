import matplotlib
from matplotlib import pyplot as plt
import os
import numpy as np
plt.ioff()

def mollweide_maps(grid, maps = ['Br_sm', 'Bth_sm', 'Bphi_sm', 'measurements_counts'], maps_names = [r"$B_{r}$", r"$B_{\theta}$", r"$B_{\phi}$", "counts/bin"], cb_names = [r"$B \, [nT]$", ""], 
                   fts = 14, hw = 3, hl = 4, hal = 5, plots_path = f"../plots", map_type_name='magnetic_field',save = False, cb_lim = None):

    y_ticks_deg = [r"$45 \degree $ S", "0", r"$45 \degree $ N"]
    y_ticks = list(np.deg2rad([-45, 0, 45]))

    x_ticks_deg = [-135, -90, -45, 0, 45, 90, 135]
    x_ticks = list(np.deg2rad(x_ticks_deg))

    th_mol = -(grid.th_2d - np.pi / 2)
    phi_mol = grid.phi_2d + (np.sign(np.pi - grid.phi_2d) - 1) * np.pi
    
    m = [getattr(grid, maps_i) for maps_i in maps]

    if save:
            
        plots_path_date = os.path.abspath(f"{plots_path}/{grid.data}_dr_{grid.dr}_dth_{grid.dth_deg}_dphi_{grid.dphi_deg}_{map_type_name}")
        if not os.path.isdir(plots_path_date):
            os.makedirs(plots_path_date)
                
    for ir in range(len(grid.r)):

        fig, ax = plt.subplots(
            nrows=1, ncols=len(maps), figsize=(6.5*len(maps), 5), subplot_kw={"projection": "mollweide"}
        )
        
        u = [m_i[:, :, ir] for m_i in m]
        
        comp_max = max(np.nanmax(u[0]), np.nanmax(u[1]), np.nanmax(u[2]))
        comp_min = min(np.nanmin(u[0]), np.nanmin(u[1]), np.nanmin(u[2]))
        cb_max = max(abs(comp_max), abs(comp_min))/1.2
        
        cbar_lim = [-cb_max, cb_max] if cb_lim == None else cb_lim
        
        for i in range(3):
    
            cmesh = ax[i].pcolormesh(
                phi_mol[:, :, ir],
                th_mol[:, :, ir],
                u[i],
                cmap="RdBu_r",
                vmin=cbar_lim[0],
                vmax=cbar_lim[1],
                alpha=1,
            )
            
            quiv = ax[i].quiver(
                phi_mol[:, :, ir],
                th_mol[:, :, ir],
                u[2],
                -u[1],
                headwidth=hw,
                headaxislength=hal,
                headlength=hl,
            )
            
            ax[i].set_title(maps_names[i], fontsize = fts)
            ax[i].set_xlabel(r"$Lon_{MSE}\,  [\degree] $", fontsize = fts)
            ax[i].set_ylabel(r"$Lat_{MSE} \, [\degree]$", fontsize = fts)
            ax[i].set_xticks(ticks=x_ticks, labels=x_ticks_deg)
            ax[i].set_yticks(ticks=y_ticks, labels=y_ticks_deg)
            
            ax[i].grid(color="black", linestyle="--", alpha=0.5)
            gridlines = ax[i].xaxis.get_gridlines()
            gridlines[1].set_linestyle('-')
            gridlines[1].set_color("orange")
            gridlines[1].set_linewidth(3)
            gridlines[5].set_linestyle('-')
            gridlines[5].set_color("orange")
            gridlines[5].set_linewidth(3)
            
        cb_maps = fig.colorbar(
            mappable=cmesh,
            ax=ax[:3],
            orientation="horizontal",
            shrink=0.4,
        )
        cb_maps.set_label(label=cb_names[0],fontsize = fts)
        
        if len(maps) == 4:

            if maps[3] in ["divB_curlB"]:
                vmin = 0; vmax = 1
            else:
                vmin = None; vmax = None
            
            map4 = ax[3].pcolormesh(phi_mol[:, :, ir], th_mol[:, :, ir], u[3], vmin = vmin, vmax = vmax)
                
            ax[3].set_title(maps_names[3], fontsize = fts)
            ax[3].set_xlabel(r"$Lon_{MSE}\,[ \degree] $", fontsize = fts)
            ax[3].set_ylabel(r"$Lat_{MSE} \, [\degree]$", fontsize = fts)
            ax[3].set_xticks(ticks=x_ticks, labels=x_ticks_deg)
            ax[3].set_yticks(ticks=y_ticks, labels=y_ticks_deg)
            
            ax[3].grid(color="black", linestyle="--", alpha=0.5)
            gridlines = ax[3].xaxis.get_gridlines()
            gridlines[1].set_linestyle('-')
            gridlines[1].set_color("orange")
            gridlines[1].set_linewidth(3)
            gridlines[5].set_linestyle('-')
            gridlines[5].set_color("orange")
            gridlines[5].set_linewidth(3)

            cb_map4 = fig.colorbar(
            mappable=map4, ax=ax[3], orientation="horizontal", shrink=1.2)
            cb_map4.set_label(label=cb_names[1], fontsize = fts)
                
        [ax[i].set_facecolor("0.6") for i in range(len(ax))]
        
        plt.annotate(r'$\vec{B}_{\rm IMF}$', xy=(0.328, 0.831), xytext=(0.29, 0.831), xycoords = 'figure fraction',
                 arrowprops=dict(facecolor='red', width = 3),horizontalalignment='center',
                verticalalignment='center', fontsize = fts)
        
        fig.suptitle(
            rf"$h = {str((np.around((grid.r[ir]-1)*3396.19, 0)))} km$ $ ( r = {str(np.around(grid.r[ir], 3))} R_{{M}})$", fontsize = fts
        )
        dist = format(grid.r[ir], ".2f")

        if save:
            fig.savefig(
                f"{plots_path_date}/{map_type_name}_r_{dist}_Rm.png", bbox_inches="tight"
            )
    
    return fig, ax