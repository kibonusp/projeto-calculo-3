from manim import *

def axis_vector_field(scene: Scene, func: np.array, wait_time: int = 5):
        numberplane = NumberPlane()
        array_field = ArrowVectorField(func)

        scene.play(FadeIn(array_field), FadeIn(numberplane))

        stream_lines = StreamLines(
            func, 
            stroke_width=1,
            max_anchors_per_line=10,
            # stroke_width=3, max_anchors_per_line=5, virtual_time=1
        )

        scene.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1, time_width=0.5)
        scene.wait(wait_time)
        # scene.play(stream_lines.end_animation())
        scene.remove(stream_lines, numberplane, array_field)


class VideoMainScene(Scene):
    def construct(self):
        IntroVectorCalculus.construct(self)
        Axes3DExplanation.construct(self)
        Divergence.construct(self)        


class Axes3DExplanation(ThreeDScene):
    def construct(self):
        title = Text('Universo 2D?')
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


class VectorFieldScene(Scene):
    def construct(self):
        f1 = lambda pos: np.array([np.sin(pos[0]), pos[1] ** 2, 0])
        f2 = lambda pos: np.array([-(pos[1]), pos[0], 0])
        ftex = MathTex(r"F(x,y)").move_to(3*UR)
        f1tex = MathTex(r"F(x,y)=(\sin x, y^{2})").move_to(3*UR)
        f2tex = MathTex(r"F(x,y)=(-y, x)").move_to(3*UR)

        numberplane = NumberPlane()
        self.play(FadeIn(numberplane), FadeIn(ftex))

        self.wait(2)
        array_field1 = ArrowVectorField(f1)
        self.bring_to_back(array_field1)
        self.play(FadeIn(array_field1), Transform(ftex, f1tex))


        self.wait(3)
        array_field2 = ArrowVectorField(f2)
        self.bring_to_back(array_field2)
        self.play(Transform(array_field1, array_field2), Transform(ftex, f2tex))

        self.wait(3)

        self.remove(numberplane, array_field2, f2tex)



class Divergence(Scene):
    def construct(self):
        title = Text('Divergente')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        # self.wait(3)
        positive_div = MathTex(r"\text{div} > 0")
        positive_tex = MathTex(r"F(x, y) = (x, y)").next_to(positive_div, DOWN)
        positive_group = VGroup(positive_div, positive_tex)
        self.play(Write(positive_group))
        self.wait(2)
        self.play(FadeOut(positive_group))

        positive_func = lambda pos: np.array([pos[0], pos[1], 0])
        axis_vector_field(self, positive_func)

        negative_div = MathTex(r"\text{div} < 0")
        negative_tex = MathTex(r"F(x, y) = (-x, -y)").next_to(negative_div, DOWN)
        negative_group = VGroup(negative_div, negative_tex)
        self.play(Write(negative_group))
        self.wait(2)
        self.play(FadeOut(negative_group))

        negative_func = lambda pos: np.array([-pos[0], -pos[1], 0])
        axis_vector_field(self, negative_func)


class Gradiente(Scene):
    def construct(self):
        title = Text('Gradiente')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        grad = MathTex(r"\nabla = (\frac{\partial }{\partial x}, \frac{\partial }{\partial y})")
        self.play(Write(grad))
        self.wait(2)
        self.play(FadeOut(grad))

        grad_div = MathTex(r"\text{div} F = \nabla \cdot F")
        self.play(Write(grad_div))
        self.wait(2)
        self.play(FadeOut(grad_div))


class NavierStokes(Scene):
    def construct(self):
        title = Text('Equações de fluidos incompressíveis')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        t1 = MathTex(r"u: \text{ Campo de velocidade}")
        t2 = MathTex(r"p: \text{ Campo de pressão}")
        t3 = MathTex(r"t: \text{ Tempo}")
        t4 = MathTex(r"\nu: \text{ Viscosidade}")
        t5 = MathTex(r"\rho: \text{ Densidade do fluido}")
        t6 = MathTex(r"f: \text{ Forças externas}")
        x = VGroup(t1, t2, t3, t4, t5, t6).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.7)
        x.set_opacity(0.5)
        self.play(FadeIn(x))

        self.wait()
        t1.set_opacity(1)

        self.wait()
        t2.set_opacity(1)
        t1.set_opacity(0.5)

        self.wait()
        t3.set_opacity(1)
        t2.set_opacity(0.5)

        self.wait()
        t4.set_opacity(1)
        t3.set_opacity(0.5)

        self.wait()
        t5.set_opacity(1)
        t4.set_opacity(0.5)

        self.wait()
        t6.set_opacity(1)
        t5.set_opacity(0.5)

        self.wait()
        t6.set_opacity(0.5)
        self.wait()
        self.play(FadeOut(x))


        ns_equation = MathTex(r"\frac{\partial u}{\partial t}", "=", 
            r"-(u \cdot \nabla)u", "-", r"\frac{1}{\rho}\nabla p", "+", r"\nu \nabla ^ 2 u", 
            "+", "f")
        div0 = MathTex(r"\nabla \cdot u = 0")

        ut_box = SurroundingRectangle(ns_equation[0], buff = .1)
        div_box = SurroundingRectangle(ns_equation[2], buff = .1)
        in_force_box = SurroundingRectangle(ns_equation[4], buff = .1)
        diff_box = SurroundingRectangle(ns_equation[6], buff = .1)
        ex_force_box = SurroundingRectangle(ns_equation[8], buff = .1)
        
        both_eq = VGroup(ns_equation.shift(UP), div0.shift(DOWN))

        self.play(Write(both_eq))
        self.wait(2)
        self.play(FadeOut(both_eq))

        self.play(Write(div0.shift(UP)))
        self.wait(2)
        self.play(FadeOut(div0))


        self.play(Write(ns_equation.shift(DOWN)))
        self.wait()
        self.play(Create(ut_box))
        self.wait()
        self.play(ReplacementTransform(ut_box, div_box))
        self.wait()
        self.play(ReplacementTransform(div_box, in_force_box))
        self.wait()
        self.play(ReplacementTransform(in_force_box, diff_box))
        self.wait()
        self.play(ReplacementTransform(diff_box, ex_force_box))
        self.wait()



        






