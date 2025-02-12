default:
    spack env activate -d . && spack concretize --fresh --deprecated --force && spack install -y
