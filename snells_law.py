from manim import *
import numpy as np


class SnellsLawDemo(Scene):
    def __init__(self):
        super().__init__()
        # Configuration constants
        self.n1 = 1.0  # Refractive index of air
        self.n2 = 1.33  # Refractive index of water
        self.incident_angle = 45  # Degrees
        self.interface_y = 0  # Y-coordinate of the interface
        self.ray_length = 2  # Length of the arrows (rays)
        self.arc_radius = 0.5  # Radius of the angle arcs

    def compute_angles(self):
        """Compute the incident and refracted angles."""
        theta1 = np.deg2rad(self.incident_angle)
        try:
            theta2 = np.arcsin((self.n1 / self.n2) * np.sin(theta1))
        except ValueError:
            theta2 = np.pi / 2  # Total internal reflection case
        return theta1, theta2

    def create_medium_backgrounds(self):
        """Create distinct backgrounds for the two mediums."""
        medium1 = Rectangle(
            width=8,
            height=4,
            fill_color=BLUE_E,  # Softer blue for air
            fill_opacity=0.1,
            stroke_width=0
        ).shift(UP * (self.interface_y + 2))

        medium2 = Rectangle(
            width=8,
            height=4,
            fill_color=BLUE_D,  # Darker blue for water
            fill_opacity=0.2,
            stroke_width=0
        ).shift(DOWN * (2 - self.interface_y))

        return VGroup(medium1, medium2)

    def create_interface_line(self):
        """Create the interface line between mediums."""
        return Line(
            start=np.array([-4, self.interface_y, 0]),
            end=np.array([4, self.interface_y, 0]),
            stroke_width=2,
            color=WHITE
        )

    def create_rays(self, theta1, theta2):
        """Create incident and refracted rays."""
        start_point = np.array(
            [-self.ray_length * np.cos(theta1), self.ray_length * np.sin(theta1), 0]
        )
        intersection_point = np.array([0, 0, 0])

        # Create incident ray
        incident_ray = Arrow(
            start=start_point,
            end=intersection_point,
            color=YELLOW,
            stroke_width=3,  # Thinner arrow
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )

        # Create refracted ray
        refracted_ray = Arrow(
            start=intersection_point,
            end=intersection_point + self.ray_length * np.array([np.sin(theta2), -np.cos(theta2), 0]),
            color=ORANGE,
            stroke_width=3,  # Thinner arrow
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )

        return VGroup(incident_ray, refracted_ray), intersection_point

    def create_normal_and_angles(self, intersection_point, theta1, theta2):
        """Create normal line and angle arcs."""
        # Normal line
        normal = DashedLine(
            start=intersection_point + UP * 2,
            end=intersection_point + DOWN * 2,
            color=TEAL,
            dash_length=0.1,
            stroke_width=2
        )

        # Create angle arcs
        theta1_arc = Arc(
            radius=self.arc_radius,
            start_angle=PI / 2,  # Starting from the normal (up)
            angle=theta1,
            color=MAROON,
            stroke_width=2
        )

        theta2_arc = Arc(
            radius=self.arc_radius,
            start_angle=-PI / 2,  # Starting from the normal (down)
            angle=theta2,
            color=MAROON,
            stroke_width=2
        )

        return VGroup(normal, theta1_arc, theta2_arc)

    def create_labels(self, intersection_point, theta1, theta2):
        """Create all text labels with improved positioning for angle labels."""
        # Label for θ₁ - Adjusted position to be closer to the arc
        theta1_label = MathTex(r"\theta_1", color=MAROON).scale(0.8)
        # Position adjusted to be closer to the arc, slightly right of the arc's midpoint
        theta1_label.move_to(
            intersection_point + 
            self.arc_radius * 1.5 * np.array([
                np.cos(theta1/2 + PI/2),  # Rotated by 90 degrees (PI/2)
                np.sin(theta1/2 + PI/2),
                0
            ])
        )

        # Label for θ₂ - Adjusted position to be closer to the arc
        theta2_label = MathTex(r"\theta_2", color=MAROON).scale(0.8)
        # Position adjusted to be closer to the arc, slightly right of the arc's midpoint
        theta2_label.move_to(
            intersection_point + 
            self.arc_radius * 1.5 * np.array([
                np.cos(theta2/2 - PI/2),  # Rotated by -90 degrees (-PI/2)
                np.sin(-theta2/2 - PI/2),
                0
            ])
        )

        # Medium labels
        medium1_label = Text("Air (n₁ = 1.0)", font_size=24, color=WHITE).shift(UP * 2.5)
        medium2_label = Text("Water (n₂ = 1.33)", font_size=24, color=WHITE).shift(DOWN * 2.5)

        # Snell's law equation
        equation = MathTex(
            r"n_1 \sin(\theta_1) = n_2 \sin(\theta_2)",
            font_size=36,
            color=WHITE
        ).to_edge(UP)

        return VGroup(medium1_label, medium2_label, theta1_label, theta2_label, equation)


    def construct(self):
        """Construct the full animation."""
        # Precompute angles
        theta1, theta2 = self.compute_angles()

        # Create all elements
        backgrounds = self.create_medium_backgrounds()
        interface = self.create_interface_line()
        rays, intersection_point = self.create_rays(theta1, theta2)
        angles_and_normal = self.create_normal_and_angles(intersection_point, theta1, theta2)
        labels = self.create_labels(intersection_point, theta1, theta2)

        # Animation sequence
        self.play(FadeIn(backgrounds))
        self.play(Create(interface))
        self.play(Create(angles_and_normal[0]))  # Normal line
        self.play(Create(rays[0]))  # Incident ray
        self.play(
            Create(angles_and_normal[1]),  # Theta 1 arc
            Write(labels[2])  # Theta 1 label
        )
        self.play(Create(rays[1]))  # Refracted ray
        self.play(
            Create(angles_and_normal[2]),  # Theta 2 arc
            Write(labels[3])  # Theta 2 label
        )
        self.play(
            Write(labels[0]),  # Medium 1 label
            Write(labels[1])   # Medium 2 label
        )
        self.play(Write(labels[4]))  # Equation
        self.wait(2)
