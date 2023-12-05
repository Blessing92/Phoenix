#!/bin/bash


#CPU performance test using sysbench
sysbench --test=cpu --cpu-max-prime=20000 run > cpu_test_results.txt