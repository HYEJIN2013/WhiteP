#!/usr/bin/python

import argparse
import os
import sys


# TODO: Figure out how to match up libraries with versions properly so we can
# find out really for real which libraries are fouund by one but not the
# other.

# TODO: For libraries that they both have, do they support the same
# dependencies?

# TODO: For packages that they both have, do they support the same libraries?


def make_arg_parser():
    p = argparse.ArgumentParser()
    p.add_argument('apt_file_db', type=argparse.FileType('r'))
    p.add_argument('lib_dep_db', type=argparse.FileType('r'))
    return p


def parse_csv(stream):
    for line in stream:
        yield line.strip().split(',')


def load_db(stream):
    db = []
    for row in parse_csv(stream):
        db.append(
            {'library': row[1],
             'package': row[0],
             'architecture': row[3]})
    return db


def filter_libraries(libs):
    filtered = []
    for lib in sorted(libs, reverse=True):
        if filtered and filtered[-1].startswith(lib):
            continue
        filtered.append(lib)
    return sorted(filtered)


def unroll_library(lib):
    if not (lib.startswith('lib') and '.so.' in lib):
        yield lib
        return
    while not lib.endswith('.so'):
        yield lib
        lib, version = os.path.splitext(lib)
    yield lib


def unroll_libraries(libs):
    unrolled = []
    for lib in libs:
        unrolled.extend(unroll_library(lib))
    return unrolled


def get_libraries(db, arch):
    return set(row['library'] for row in db if row['architecture'] == arch)


def get_packages(db):
    return set(row['package'] for row in db if not row['package'].endswith('-dev'))


def dump_list(name, sequence, output):
    def w(line):
        output.write(line)
        output.write('\n')
        output.flush()
    data = sorted(sequence)
    title = '%s (%s)' % (name, len(data))
    write_underline(title, '-', output)
    for datum in data:
        w(datum)
    w('')


def write_underline(title, character, output):
    output.write(title)
    output.write('\n')
    output.write(character * len(title))
    output.write('\n')
    output.write('\n')


def write_comparison(title, a_title, a_set, b_title, b_set, output):
    write_underline(title, '=', output)
    dump_list(a_title, a_set - b_set, output)
    dump_list(b_title, b_set - a_set, output)


def library_differences(arch, apt_file_db, lib_dep_db, output):
    apt_file_libs = set(unroll_libraries(get_libraries(apt_file_db, arch)))
    lib_dep_libs = set(unroll_libraries(get_libraries(lib_dep_db, arch)))
    write_comparison(
        '%s libraries' % (arch,),
        'apt-file only', apt_file_libs,
        'lib-dep only', lib_dep_libs,
        output)


def packages_differences(apt_file_db, lib_dep_db, output):
    write_underline('packages', '=', output)
    apt_file_pkgs = get_packages(apt_file_db)
    lib_dep_pkgs = get_packages(lib_dep_db)
    write_comparison(
        'packages',
        'apt-file only', apt_file_pkgs,
        'lib-dep only', lib_dep_pkgs,
        output)


def report_differences(apt_file_db, lib_dep_db, output):
    library_differences('i386', apt_file_db, lib_dep_db, output)
    packages_differences(apt_file_db, lib_dep_db, output)


def one_arch_only():
    """
    For a single database, show which libraries appear for one architecture
    only.
    """
    db = load_db(open(sys.argv[1], 'r'))
    i386 = get_libraries(db, 'i386')
    amd64 = get_libraries(db, 'amd64')
    write_comparison(
        'Libraries by architecture',
        'i386 only', i386 - amd64,
        'amd64 only', amd64 - i386,
        sys.stdout)


def whitelist():
    """Print out a packaging whitelist.
    All packages found that contain libraries that don't start with 'lib'.
    """
    parser = make_arg_parser()
    args = parser.parse_args()
    apt_file_db = load_db(args.apt_file_db)
    lib_dep_db = load_db(args.lib_dep_db)
    packages = get_packages(apt_file_db) - get_packages(lib_dep_db)
    for package in packages:
        if package.startswith('lib'):
            continue
        print package


def main():
    parser = make_arg_parser()
    args = parser.parse_args()
    apt_file_db = load_db(args.apt_file_db)
    lib_dep_db = load_db(args.lib_dep_db)
    report_differences(apt_file_db, lib_dep_db, sys.stdout)
    return 0


if __name__ == '__main__':
    sys.exit(main())
