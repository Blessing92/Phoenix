# Phoenix

# Installing NumPy in Alpine Linux

This guide provides instructions for installing NumPy in an Alpine Linux environment using a virtual environment.

## Prerequisites

Make sure you have the following installed:
- Alpine Linux
- `apk` package manager

## Steps

1. Update the package index:

    ```bash
    apk update
    ```

2. Install the required build dependencies:

    ```bash
    apk add build-base ninja patchelf gfortran openblas-dev openmpi openmpi-dev

    ```

3. Create a virtual environment:

    ```bash
    python3 -m venv /path/to/venv
    ```

    Replace `/path/to/venv` with the desired location for your virtual environment.

4. Activate the virtual environment:

    ```bash
    source /path/to/venv/bin/activate

    ```

5. Install NumPy Scipy MPI using pip within the virtual environment:

    ```bash
    pip install numpy
    ```

    ```bash
    pip install scipy
    ```

     ```bash
    pip install mpi4py
    ```

6. Verify the installation:

    ```bash
    python -c "import numpy; print(numpy.__version__)"
    ```

    This should print the version of NumPy without errors.

7. Deactivate the virtual environment:

    ```bash
    deactivate
    ```

By following these steps, you create an isolated environment for your project, preventing conflicts with the system-wide Python packages. Activate the virtual environment using `source /path/to/venv/bin/activate` before running your Python script.



