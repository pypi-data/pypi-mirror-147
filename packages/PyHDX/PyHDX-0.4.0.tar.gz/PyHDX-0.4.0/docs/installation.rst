============
Installation
============

Currently the recommended version to use is the latest beta release (v0.4.0bx)

Stable release
--------------

Installation with `conda`:

.. code-block:: rst

   $ conda install -c conda-forge pyhdx

Installation with `pip`:

.. code-block:: rst

   $ pip install pyhdx

To install with web application:

.. code-block:: rst

    $ pip install pyhdx[web]

To install with pdf output:

.. code-block:: rst

    $ pip install pyhdx[pdf]


Install from source
-------------------

Create a new conda environment:

.. code-block::

    $ conda create --name py38_pyhdx python=3.8
    # conda activate py38_pyhdx

Clone the github repository:

.. code-block:: rst

    $ git clone https://github.com/Jhsmit/PyHDX
    $ cd PyHDX

Generate conda requirements files from `setup.cfg`:

.. code-block:: rst

    $ python _requirements.py

Install the base dependencies and optional extras. For example, to install PyHDX with web app:

.. code-block:: rst

    $ conda install --file _req-base.txt --file _req-web.txt

To run the web application:

.. code-block::

    $ python pyhdx/web/serve.py

This runs the pyhx web application without a Dask cluster to submit jobs to, so
submitting a fitting job will give an error.

To start a dask cluster separately, open another terminal tab and run:

.. code-block:: rst

    python local_cluster.py



Running the web server
----------------------

PyHDX web application can be launched from the command line using ``pyhdx`` command with below options,

To run PyHDX server using default settings on your local server:

.. code-block:: rst

    $ pyhdx serve

To run PyHDX server using the IP address and port number of your dask cluster:

.. code-block:: rst

    $ pyhdx serve --scheduler_address <ip>:<port>

If no dask cluster is found at the specified address, a LocalCluster will be started (on localhost) using the
specified port number.

To start a dask cluster separately, open another terminal tab and run:

.. code-block:: rst

    python local_cluster.py

This will start a Dask cluster on the scheduler address as specified in the PyHDX config.
(user dir / .pyhdx folder)


Install from source
-------------------

Clone the github repository:

.. code-block:: rst

    $ git clone https://github.com/Jhsmit/PyHDX
    $ cd PyHDX

You can use one of the files in 'dev/deps/pinned' to install a pretested set of pinned
dependencies.

With `pip`:

.. code-block:: rst

    $ pip install -r dev/deps/pinned/py38_windows_pip.txt

Or use 'py38_linux_pip.txt', which should be the same.

With `conda`:

.. code-block:: rst

    $ conda env create -f dev/deps/pinned/py38_windows_conda.yml

Otherwise, you try your luck with the latest versions of the dependencies.
If you would like a specific PyTorch version to use with PyHDX (ie CUDA/ROCm support), you should install this first.
Installation instructions are on the Pytorch_ website.

Then, install the other base dependencies and optional extras.

Create a new conda environment:

.. code-block::

    $ conda create --name py38_pyhdx python=3.8
    # conda activate py38_pyhdx

To install all dependencies:

.. code-block:: rst

    $ conda install --file req-all.txt

Or choose which extras to install by using the 'req-<extra>.txt' files.

Install PyHDX in develop/editable mode

.. code-block:: rst

    conda develop .

To run the web application:

.. code-block::

    $ python pyhdx/web/serve.py

This runs the pyhx web application without a Dask cluster to submit jobs to, so
submitting a fitting job will give an error.

To start a dask cluster separately, open another terminal tab and run:

.. code-block:: rst

    python local_cluster.py


Dependencies
------------

The requirements for PyHDX and its extras are listed in setup.cfg

.. _Github repo: https://github.com/Jhsmit/pyhdx

.. _Pytorch: https://pytorch.org/
