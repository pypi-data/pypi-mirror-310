# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
import datetime as dt
from math import floor


def factorize(n):
    assert n != 0, "Cannot factorize zero."

    while n % 2 == 0:
        n //= 2
        yield 2

    for div in range(3, int(n**0.5) + 1, 2):
        while n % div == 0:
            n //= div
            yield div

        if n == 1:
            return

    if n > 1:
        yield n


def fortran_array(lst):
    assert all(isinstance(i, int) for i in lst)

    elems = []

    prev = 0.5
    acc = 0
    for e in lst:
        if e == prev:
            acc += 1
        else:
            if acc:
                elems.append(f"{acc}*{float(prev):.01f}")
            prev = e
            acc = 1

    if acc:
        elems.append(f"{acc}*{float(prev):.01f}")

    return " ".join(elems)


def naturaldelta(delta: dt.timedelta) -> str:
    assert isinstance(delta, dt.timedelta)

    days = abs(delta.days)
    seconds = abs(delta.seconds)
    microseconds = abs(delta.microseconds)

    years = days / 365

    if years > 2:
        years = int(floor(years))
        months = int(round(days / 30.5)) - 12 * years

        if months == 0:
            return f"{years} years"
        elif months == 1:
            return f"{years} years, one month"
        else:
            return f"{years} years, {months} months"

    months = days / 30.5

    if months > 2:
        return simplefraction(months, "months")

    frac_days = days + seconds / (3600 * 24)

    if frac_days > 2:
        return simplefraction(frac_days, "days")

    hours = 24 * days + seconds / 3600

    if hours > 2:
        return simplefraction(hours, "hours")

    minutes = seconds / 60

    if minutes > 2:
        return simplefraction(minutes, "minutes")

    frac_seconds = seconds + microseconds / 1e6
    if frac_seconds > 2:
        return simplefraction(frac_seconds, "seconds")

    milliseconds = 1000 * seconds + microseconds / 1000

    if milliseconds > 500:
        return f"{0.1:f} seconds"

    if milliseconds > 2:
        return f"{int(round(milliseconds))} ms"

    if microseconds > 500:
        return f"{milliseconds:0.1f} ms"

    return f"{microseconds} us"


def simplefraction(n, name):
    assert n > 1
    if n > 9:
        return f"{int(round(n))} {name}"

    left = int(round(2 * n) - 2 * floor(n))
    if left == 0:
        return f"{int(floor(n))} {name}"
    elif left == 1:
        return f"{int(floor(n))} and a half {name}"
    else:
        return f"{int(round(n))} {name}"


class InvalidInput(ValueError):
    pass


try:
    from math import prod
except ImportError:

    def prod(numbers):
        t = 1
        for n in numbers:
            t *= n
        return t


electronegativity = {
    # Pauling electronegativity, or 10.0 for species where
    # no data is available
    "H": 2.20,
    "He": 10.0,
    "Li": 0.98,
    "Be": 1.57,
    "B": 2.04,
    "C": 2.55,
    "N": 3.04,
    "O": 3.44,
    "F": 3.98,
    "Ne": 10.0,
    "Na": 0.93,
    "Mg": 1.31,
    "Al": 1.61,
    "Si": 1.90,
    "P": 2.19,
    "S": 2.58,
    "Cl": 3.16,
    "Ar": 10.0,
    "K": 0.82,
    "Ca": 1.00,
    "Sc": 1.36,
    "Ti": 1.54,
    "V": 1.63,
    "Cr": 1.66,
    "Mn": 1.55,
    "Fe": 1.83,
    "Co": 1.88,
    "Ni": 1.91,
    "Cu": 1.90,
    "Zn": 1.65,
    "Ga": 1.81,
    "Ge": 2.01,
    "As": 2.18,
    "Se": 2.55,
    "Br": 2.96,
    "Kr": 3.00,
    "Rb": 0.82,
    "Sr": 0.95,
    "Y": 1.22,
    "Zr": 1.33,
    "Nb": 1.6,
    "Mo": 2.16,
    "Tc": 1.9,
    "Ru": 2.2,
    "Rh": 2.28,
    "Pd": 2.20,
    "Ag": 1.93,
    "Cd": 1.69,
    "In": 1.78,
    "Sn": 1.96,
    "Sb": 2.05,
    "Te": 2.1,
    "I": 2.66,
    "Xe": 2.6,
    "Cs": 0.79,
    "Ba": 0.89,
    "La": 1.10,
    "Ce": 1.12,
    "Pr": 1.13,
    "Nd": 1.14,
    "Pm": 1.13,
    "Sm": 1.17,
    "Eu": 1.2,
    "Gd": 1.2,
    "Tb": 1.22,
    "Dy": 1.23,
    "Ho": 1.24,
    "Er": 1.24,
    "Tm": 1.25,
    "Yb": 1.1,
    "Lu": 1.27,
    "Hf": 1.3,
    "Ta": 1.5,
    "W": 2.36,
    "Re": 1.9,
    "Os": 2.2,
    "Ir": 2.2,
    "Pt": 2.28,
    "Au": 2.54,
    "Hg": 2.00,
    "Tl": 1.62,
    "Pb": 2.33,
    "Bi": 2.02,
    "Po": 2.0,
    "At": 2.2,
    "Rn": 10.0,
    "Fr": 0.7,
    "Ra": 0.89,
    "Ac": 1.1,
    "Th": 1.3,
    "Pa": 1.5,
    "U": 1.38,
    "Np": 1.36,
    "Pu": 1.28,
    "Am": 1.3,
    "Cm": 1.3,
    "Bk": 1.3,
    "Cf": 1.3,
    "Es": 1.3,
    "Fm": 1.3,
    "Md": 1.3,
    "No": 1.3,
    "Lr": 10.0,
    "Rf": 10.0,
    "Db": 10.0,
    "Sg": 10.0,
    "Bh": 10.0,
    "Hs": 10.0,
    "Mt": 10.0,
    "Ds": 10.0,
    "Rg": 10.0,
    "Cn": 10.0,
    "Nh": 10.0,
    "Fl": 10.0,
    "Mc": 10.0,
    "Lv": 10.0,
    "Ts": 10.0,
    "Og": 10.0,
}
