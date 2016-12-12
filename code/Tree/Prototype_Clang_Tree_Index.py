class ClangFileToIndex(File_To_Index):
    pass # ClangFileToIndex definition


def env(vars_, tree):
    # Setup environment variables for inspecting clang as runtime
    # We'll store all the havested metadata in the plugins temporary folder.
    temp_folder = os.path.join(tree.temp_folder, 'plugins', PLUGIN_NAME)
    plugin_folder = os.path.join(tree.config.plugin_folder, PLUGIN_NAME)
    flags = [
        '-load', os.path.join(plugin_folder, 'libclang-index-plugin.so'),
        '-add-plugin', 'dxr-index',
        '-plugin-arg-dxr-index', tree.source_folder
    ]
    flags_str = ""
    for flag in flags:
        flags_str += ' -Xclang ' + flag
    env = {
        'CC': "clang %s" % flags_str,
        'CXX': "clang++ %s" % flags_str,
        'DXR_CLANG_FLAGS': flags_str,
        'DXR_CXX_CLANG_OBJECT_FOLDER': tree.object_folder,
        'DXR_CXX_CLANG_TEMP_FOLDER': temp_folder,
    }
    env['DXR_CC'] = env['CC']
    env['DXR_CXX'] = env['CXX']

    return merge(vars_, env)


@tree_to_indexer # Creates TreeIndexer
def clang_indexer(tree):
    vars_ = yield
    # Env setup
    yield env(vars_, tree)

    # PREBUILD

    yield # BUILD STEP
    
    # POST BUILD

    # Build up only the inheritance part of the CSV
    condensed = load_csv(temp_folder, csv_path=None, only_impl=True)
    inherit = build_inhertitance(condensed)

    yield partial(ClangFileToIndex, inherit)
