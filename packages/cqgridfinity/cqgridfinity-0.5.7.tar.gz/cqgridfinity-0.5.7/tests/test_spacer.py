# Gridfinity tests
import datetime

# my modules
from cadquery import exporters
from cqgridfinity import *
from cqkit.cq_helpers import size_3d
from cqkit import export_step_file

from common_test import EXPORT_STEP_FILE_PATH, _almost_same, _export_files, INCHES


def test_spacer():
    s0 = GridfinityDrawerSpacer(582, 481, tolerance=0.25)
    assert s0.size_u[0] == 13
    assert s0.size_u[1] == 11
    assert s0.length_u == 4
    assert s0.width_u == 3
    assert s0.length_fill == 5 * GRU
    assert s0.width_fill == 5 * GRU
    assert s0.wide_enough
    assert s0.deep_enough
    assert _almost_same(s0.length_th, 9.25, tol=0.01)
    assert _almost_same(s0.width_th, 17.75, tol=0.01)

    s1 = GridfinityDrawerSpacer(tolerance=0.25)
    s1.best_fit_to_dim(582, 300)
    assert s1.size_u[0] == 13
    assert s1.size_u[1] == 7
    assert s1.width_u == 2
    assert s1.width_fill == 3 * GRU
    assert s1.wide_enough
    assert not s1.deep_enough

    s1.best_fit_to_dim(300, 582)
    assert s1.size_u[0] == 7
    assert s1.size_u[1] == 13
    assert s1.length_u == 2
    assert s1.length_fill == 3 * GRU
    assert not s1.wide_enough
    assert s1.deep_enough

    s1.best_fit_to_dim(INCHES(11.5), INCHES(20.5))
    assert s1.size_u[0] == 6
    assert s1.size_u[1] == 12
    assert s1.length_u == 2
    assert s1.width_u == 4
    assert s1.length_fill == 2 * GRU
    assert s1.width_fill == 4 * GRU
    assert s1.wide_enough
    assert s1.deep_enough
    assert _almost_same(s1.length_th, 8.10, tol=0.01)
    assert _almost_same(s1.width_th, 19.80, tol=0.01)


def test_spacer_render():
    s1 = GridfinityDrawerSpacer(tolerance=0.25)
    dx, dy = INCHES(22 + 15 / 16), INCHES(16.25)
    s1.best_fit_to_dim(dx, dy)
    assert s1.size_u[0] == 13
    assert s1.size_u[1] == 9
    assert s1.length_u == 4
    assert s1.width_u == 3
    assert s1.length_fill == 5 * GRU
    assert s1.width_fill == 3 * GRU
    assert s1.wide_enough
    assert s1.deep_enough
    assert _almost_same(s1.length_th, 17.12, tol=0.01)
    assert _almost_same(s1.width_th, 18.06, tol=0.01)
    r = s1.render_full_set()
    assert _almost_same(size_3d(r), (582.6125, 412.75, 4.75))
    assert s1.filename() == "gf_drawer_4x3_full_set"
    if _export_files("spacer"):
        s1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    rh = s1.render_half_set()
    assert _almost_same(size_3d(rh), (253.084, 177.0625, 4.75))
    assert s1.filename() == "gf_drawer_4x3_half_set"
    if _export_files("spacer"):
        s1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    r = s1.render_length_filler()
    assert s1.filename() == "gf_drawer_4x3_length_spacer"
    if _export_files("spacer"):
        s1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    r = s1.render_width_filler()
    assert s1.filename() == "gf_drawer_4x3_width_spacer"
    if _export_files("spacer"):
        s1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    r = s1.render()
    assert s1.filename() == "gf_drawer_4x3_corner_spacer"
    if _export_files("spacer"):
        s1.save_step_file(path=EXPORT_STEP_FILE_PATH)


# def test_spacer_render():
#     s1 = GridfinityDrawerSpacer(tolerance=0.25)
#     dx, dy = INCHES(22 + 7 / 8) - 0.5, INCHES(16 + 3 / 16) - 0.5
#     s1.best_fit_to_dim(dx, dy, verbose=True)
#     rh = s1.render_half_set()
#     #     assert _almost_same(size_3d(rh), (253.084, 177.0625, 5))
#     # assert s1.filename() == "gf_drawer_4x3_half_set"
#     # if _export_files("spacer"):
#     s1.save_step_file(path=EXPORT_STEP_FILE_PATH)
