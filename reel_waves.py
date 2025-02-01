from manim import *

class WaveReel(Scene):
    def construct(self):
        freq = 5
        amp = 0.6
        wave_span = 4
        recoil_distance = 3
        wave_centers = [LEFT*recoil_distance, RIGHT*recoil_distance]

        sine_wave = FunctionGraph(
            lambda x: amp * np.sin(freq * x),
            x_range=[-wave_span/2, wave_span/2],
            color=BLUE
        ).shift(LEFT*6)

        cosine_wave = FunctionGraph(
            lambda x: amp * np.cos(freq * x),
            x_range=[-wave_span/2, wave_span/2],
            color=RED
        ).shift(RIGHT*6)

        self.play(
            sine_wave.animate.shift(RIGHT*6),
            cosine_wave.animate.shift(LEFT*6),
            run_time=2.5,
            rate_func=linear
        )
        self.play(
            sine_wave.animate.shift(LEFT*recoil_distance),
            cosine_wave.animate.shift(RIGHT*recoil_distance),
            run_time=1,
            rate_func=smooth
        )
        self.play(
            Rotate(sine_wave, PI/2, about_point=sine_wave.get_center()),
            Rotate(cosine_wave, PI/2, about_point=cosine_wave.get_center()),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        phase_tracker = ValueTracker(0)

        vertical_sine = always_redraw(lambda: ParametricFunction(
            lambda t: np.array([
                recoil_distance + amp * np.sin(freq * (t - phase_tracker.get_value())),
                t,
                0
            ]),
            t_range=[-wave_span/2, wave_span/2],
            color=RED
        ))

        vertical_cosine = always_redraw(lambda: ParametricFunction(
            lambda t: np.array([
                -recoil_distance + amp * np.cos(freq * (t - phase_tracker.get_value())),
                t,
                0
            ]),
            t_range=[-wave_span/2, wave_span/2],
            color=BLUE
        ))

        self.remove(sine_wave, cosine_wave)
        self.add(vertical_sine, vertical_cosine)
        self.play(
            phase_tracker.animate.set_value(2*PI),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)

        effect_tracker = ValueTracker(0)
        max_vertical_shift = 0.2
        max_rotation = 0.1
        max_scale = 1.1

        for wave in [vertical_sine, vertical_cosine]:
            original_center = wave.get_center()
            original_height = wave.height

            wave.add_updater(lambda m: m
                             .shift(UP * max_vertical_shift * np.sin(effect_tracker.get_value()))
                             .rotate(max_rotation * np.sin(effect_tracker.get_value()), about_point=original_center)
                             .scale_to_fit_height(
                                 original_height * (1 + (max_scale-1) * 0.5 * (1 + np.sin(effect_tracker.get_value())))
                             )
                             )

        self.play(
            effect_tracker.animate.set_value(4*PI),
            run_time=5,
            rate_func=linear
        )

        self.wait(2)
