import numpy as np
import plotly.graph_objects as go
class AntoineNecklace:
    def __init__(self, N_l1=14, N_l2=14, N_l3 = 10):
        # Attributes: These are "remembered" by the class
        self.N_l1 = N_l1
        self.N_l2 = N_l2
        self.N_l3 = N_l3
        self.tilt_angle_l1 = np.pi/2
        self.tilt_angle_l2 = np.pi/2
        self.lighting = [.2,.26,.3] #highlight, edge reflection, smoothness
        self.color_alt_list = [
            [[0, '#003366'], [1, '#003366']], # deep_blue
            [[0, '#A04606'], [1, '#A04606']]  # burnt_orange
        ]
        self.color_alt_l2 = True
        self.color_alt_l3 = False
        self.color_choice = [[0, '#003366'], [1, '#003366']] #for just one color
        self.mesh_res = 30
        self.scale = 2
        self.file_name = "antoines_necklace.png"
        self.eye = [1,1,1.3]
        self.html = False
        self.opacity = 1.0
        self.background_color = "white"
        self.background_grid_color = "white"

    # INTERNAL METHODS
    def _get_small_tori_radius(self,N, parent_C):
        small_c = (parent_C*np.pi)/(.8*N)
        return small_c
    

    def rotate_coords(self,x, y, z, ax_angles):
        orig_shape = x.shape
        points = np.stack([x.flatten(), y.flatten(), z.flatten()])
        alpha, beta, gamma = ax_angles

        Rx = np.array([[1, 0, 0], [0, np.cos(alpha), -np.sin(alpha)], [0, np.sin(alpha), np.cos(alpha)]])
        Ry = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
        Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])

        R = Rz @ Ry @ Rx
        rotated_points = R @ points
        return (rotated_points[i].reshape(orig_shape) for i in range(3))

    # CORE METHODS: "Level" functions
    def get_level_zero_necklace_tori(self,level_zero_toriRadius):
        theta = np.linspace(0, 2*np.pi, self.mesh_res)
        phi = np.linspace(0, 2*np.pi, self.mesh_res)
        theta, phi = np.meshgrid(theta, phi)
        small_a = level_zero_toriRadius/6
        x = (level_zero_toriRadius + small_a * np.cos(theta)) * np.cos(phi)
        y = (level_zero_toriRadius + small_a * np.cos(theta)) * np.sin(phi)
        z = small_a * np.sin(theta)
        fig = go.Figure()
        fig.add_trace(go.Surface(x=x, y=y, z=z, showscale=False, opacity=self.opacity,lighting=dict(
            specular=self.lighting[0],     # Increases "highlight" brightness
            fresnel=self.lighting[1],      # Increases edge reflections
            roughness=self.lighting[2]     # Makes it look smoother/shinier
        ), colorscale = self.color_choice,
        lightposition=dict(x=100, y=100, z=100)))
        return fig

    def get_level_one_necklace_tori(self, parent_l1_C=14, trans = (0,0,0), global_rot = (0,0,0), construct_l2 = False, construct_l2_upper = False, construct_l2_lower = False):
        bottom_tori = []
        top_tori = []
        side_tori = []
        small_l1_c = self._get_small_tori_radius(self.N_l1, parent_l1_C)
        small_a = small_l1_c/6

        quarter_N = self.N_l1 // 4
        if (construct_l2_upper == False) and (construct_l2_lower == True):
            # The 'Arch' (Top)
            # We start a quarter-way back and go to a quarter-way forward
            range_list = [(i % self.N_l1) for i in range(-quarter_N-1, quarter_N + 2)]
            
        elif (construct_l2_upper == True) and (construct_l2_lower == False):
            # The 'Cradle' (Bottom)
            # We start where the top ended and complete the circle
            range_list = [(i % self.N_l1) for i in range(quarter_N+1, (self.N_l1 - quarter_N))]
            
        else:
            # Standalone Level 1: Full circle
            range_list = list(range(0, self.N_l1))

        for i in range_list:
            # Base angle around the necklace
            alpha = (2*np.pi * i) / (self.N_l1)
            tilt = (self.tilt_angle_l1) * (i % 2)
            theta = np.linspace(0, 2*np.pi, self.mesh_res)

            if (i % 2 == 1): # tilted
                #bottom -----------------------------------------------------------
                phi = np.linspace(-np.pi/2, np.pi/2, self.mesh_res)
                theta, phi = np.meshgrid(theta, phi)
            
                # Basic torus at origin
                x = (small_l1_c + small_a * np.cos(theta)) * np.cos(phi)
                y = (small_l1_c + small_a * np.cos(theta)) * np.sin(phi)
                z = small_a * np.sin(theta)
                
                # Apply rotations
                # First, tilt the link, then rotate it to its position on the ring
                rx, ry, rz = self.rotate_coords(x, y, z, (0, tilt, alpha))
                
                # Translate to the ring position
                tx = rx + parent_l1_C * np.cos(alpha)
                ty = ry + parent_l1_C * np.sin(alpha) 
                tz = rz + parent_l1_C * np.sin(alpha)*0 # Keep it on XY plane
                tx, ty, tz = self.rotate_coords(tx, ty, tz, global_rot)
                tx = tx + trans[0]
                ty = ty + trans[1]
                bottom_tori.append((tx, ty, tz))
                #top -----------------------------------------------------------
                phi = np.linspace(np.pi/2, 3*np.pi/2, self.mesh_res)
                theta, phi = np.meshgrid(theta, phi)
            
                # Basic torus at origin
                x = (small_l1_c + small_a * np.cos(theta)) * np.cos(phi)
                y = (small_l1_c + small_a * np.cos(theta)) * np.sin(phi)
                z = small_a * np.sin(theta)
                
                # Apply rotations
                # First, tilt the link, then rotate it to its position on the ring
                rx, ry, rz = self.rotate_coords(x, y, z, (0, tilt, alpha))
                
                # Translate to the ring position
                tx = rx + parent_l1_C * np.cos(alpha)
                ty = ry + parent_l1_C * np.sin(alpha) 
                tz = rz + parent_l1_C * np.sin(alpha)*0 # Keep it on XY plane
                tx, ty, tz = self.rotate_coords(tx, ty, tz, global_rot)
                tx = tx + trans[0]
                ty = ty + trans[1]
                top_tori.append((tx, ty, tz))
            else: #not tilted
                phi = np.linspace(0, 2*np.pi, self.mesh_res) #sideways
                theta, phi = np.meshgrid(theta, phi)
            
                # Basic torus at origin
                x = (small_l1_c + small_a * np.cos(theta)) * np.cos(phi)
                y = (small_l1_c + small_a * np.cos(theta)) * np.sin(phi)
                z = small_a * np.sin(theta)
                
                # Apply rotations
                # First, tilt the link, then rotate it to its position on the ring
                rx, ry, rz = self.rotate_coords(x, y, z, (0, tilt, alpha))
                
                # Translate to the ring position
                tx = rx + parent_l1_C * np.cos(alpha)
                ty = ry + parent_l1_C * np.sin(alpha) 
                tz = rz + parent_l1_C * np.sin(alpha)*0 # Keep it on XY plane
                tx, ty, tz = self.rotate_coords(tx, ty, tz, global_rot)
                tx = tx + trans[0]
                ty = ty + trans[1]
                side_tori.append((tx, ty, tz))
        if construct_l2 == True:
            return bottom_tori+side_tori+top_tori
        else:
            fig = go.Figure()
            tori_data = bottom_tori+side_tori+top_tori
            for x, y, z in tori_data:
                fig.add_trace(go.Surface(x=x, y=y, z=z, showscale=False, opacity=self.opacity,lighting=dict(
                    specular=self.lighting[0],     # Increases "highlight" brightness
                    fresnel=self.lighting[1],      # Increases edge reflections
                    roughness=self.lighting[2]     # Makes it look smoother/shinier
                ), colorscale = self.color_choice,
                lightposition=dict(x=100, y=100, z=100)))
            return fig

    def get_level_two_necklace_tori(self, parent_l2_C):
        #find inner 
        level_one_toriRadius = self._get_small_tori_radius(self.N_l2, parent_C = parent_l2_C)
        #we need to split into sideways and up and down
        sideways_tori = []
        upper_tori = []
        lower_tori = []
        for i in range(self.N_l2):
            alpha1 = (2 * np.pi * i) / self.N_l2
            tilt1 = (self.tilt_angle_l2)*(i%2)
            if (i%2 == 1):
                #split into upper and lower
                #alpha_top = (alpha1/2)+np.pi/2
                transx = parent_l2_C * np.cos(alpha1)
                transy = parent_l2_C * np.sin(alpha1)
                tori_data_upper = self.get_level_one_necklace_tori(parent_l1_C=level_one_toriRadius, global_rot = (0,tilt1,alpha1), trans = (transx,transy, 0), construct_l2 = True, construct_l2_upper = True)
                tori_data_lower = self.get_level_one_necklace_tori(parent_l1_C=level_one_toriRadius, global_rot = (0,tilt1,alpha1), trans = (transx,transy, 0), construct_l2 = True, construct_l2_lower = True)
                upper_tori.extend(tori_data_upper)
                lower_tori.extend(tori_data_lower)
            else: #sideways ones
                transx = parent_l2_C * np.cos(alpha1)
                transy = parent_l2_C * np.sin(alpha1)
                tori_data_sideways = self.get_level_one_necklace_tori(parent_l1_C=level_one_toriRadius, global_rot = (0,tilt1,alpha1), trans = (transx,transy, 0), construct_l2 = True)
                sideways_tori.extend(tori_data_sideways)

        tori_all = [lower_tori, sideways_tori, upper_tori]
        fig = go.Figure()
        for j in range(len(tori_all)):
            if self.color_alt_l2 == True:
                color_scale = self.color_alt_list[j%2]
            else:
                color_scale = self.color_choice
            for x, y, z in tori_all[j]:
                fig.add_trace(go.Surface(x=x, y=y, z=z, showscale=False, opacity=self.opacity,lighting=dict(
                    specular=self.lighting[0],     # Increases "highlight" brightness
                    fresnel=self.lighting[1],      # Increases edge reflections
                    roughness=self.lighting[2]     # Makes it look smoother/shinier
                ), colorscale = color_scale,
                lightposition=dict(x=100, y=100, z=100)))
        return fig
    
    def get_figure(self, fig):
        # Higher numbers move the camera further away
        # x, y, z determine the angle
        camera = dict(eye=dict(x=self.eye[0], y=self.eye[1], z=self.eye[2]), center=dict(x=0, y=0, z=0), up=dict(x=0, y=0, z=1))
        # Remove grid lines, background planes, and labels
        fig.update_layout(scene_camera=camera, width = 2600, height = 1800, scene=dict(xaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False, 
                    showbackground=False, 
                    title=''),
                    yaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False, 
                    showbackground=False, 
                    title=''),
                    zaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False, 
                    showbackground=False, 
                    title=''),aspectmode='data'),
            # Optional: Change the overall plot background color
            paper_bgcolor=self.background_color, 
            plot_bgcolor=self.background_grid_color,
            margin=dict(l=0, r=0, b=0, t=0)
        )
        #fig.show()
        print("Writing to file...")
        fig.write_image(self.file_name, scale=self.scale)
        print("Image saved successfully!")
        if self.html == True:
            print("WARNING: only small resolution and graphic load can be written as html")
            fig.write_html("necklace_render.html")
            print("Writing to html")

    # Functions meant for user to call
    def generate_level_zero(self, parent_l0_C):
        fig  = self.get_level_zero_necklace_tori(parent_l0_C)
        self.get_figure(fig)

    def generate_level_one(self, parent_l1_C):
        fig = self.get_level_one_necklace_tori(parent_l1_C)
        self.get_figure(fig)

    def generate_level_two(self, parent_l2_C):
        fig = self.get_level_two_necklace_tori(parent_l2_C)
        self.get_figure(fig)
