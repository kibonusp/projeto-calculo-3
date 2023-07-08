from manim import *

class VideoMainScene(Scene):
    def construct(self):
        IntroVectorCalculus.construct(self)
        Axes3DExplanation.construct(self)
        Divergence.construct(self)

class IntroVectorCalculus(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(
            func, stroke_width=3, max_anchors_per_line=5, virtual_time=1, color=BLUE
        )
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5, time_width=0.5)
        self.wait(18)
        self.play(stream_lines.end_animation())


class Axes3DExplanation(ThreeDScene):
    def construct(self):
        title = Text('Campo Vetorial')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex("z"))

        # 3D variant of the Dot() object
        dot = Dot3D()

        # zoom out so we see the axes
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)
        
        sphere = Sphere(radius=2, resolution=(18, 18))
        cylinder = Cylinder(radius=2, height=0.1)

        self.wait(2)

        self.play(FadeIn(sphere))

        self.wait(2)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, zoom=0.5, run_time=1.5)
        
        self.stop_ambient_camera_rotation()
        
        self.play(FadeTransform(sphere, cylinder))

        self.wait(2)


class Divergence(Scene):
    def axis_vector_field(self, func: np.array):
        numberplane = NumberPlane()
        array_field = ArrowVectorField(func)

        self.play(FadeIn(array_field), FadeIn(numberplane))
        self.wait(3)

        stream_lines = StreamLines(
            func, 
            stroke_width=1,
            max_anchors_per_line=10,
            # stroke_width=3, max_anchors_per_line=5, virtual_time=1
        )

        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1, time_width=0.5)
        self.wait(5)
        # self.play(stream_lines.end_animation())
        self.remove(stream_lines, numberplane, array_field)


    def construct(self):
        title = Text('Divergente')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        # self.wait(3)
        positive_div = MathTex(r"\text{div} > 0")
        positive_tex = MathTex(r"F(x, y) = (x, y)").next_to(positive_div, DOWN)
        positive_group = VGroup(positive_div, positive_tex)
        self.play(FadeIn(positive_group))
        self.wait(2)
        self.play(FadeOut(positive_group))

        positive_func = lambda pos: np.array([pos[0], pos[1], 0])
        self.axis_vector_field(positive_func)

        negative_div = MathTex(r"\text{div} < 0")
        negative_tex = MathTex(r"F(x, y) = (-x, -y)").next_to(negative_div, DOWN)
        negative_group = VGroup(negative_div, negative_tex)
        self.play(FadeIn(negative_group))
        self.wait(2)
        self.play(FadeOut(negative_group))

        negative_func = lambda pos: np.array([-pos[0], -pos[1], 0])
        self.axis_vector_field(negative_func)



