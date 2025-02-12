default:
    eval `spack env activate --sh -d .` && spack concretize --fresh --deprecated --force && spack install -y
