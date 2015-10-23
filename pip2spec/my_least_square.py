import sys
from fuzzywuzzy import fuzz
import re
import pdb


def fuzzy_search_func(new_pip_name, new_name, a, b, c, d):
  return (a * fuzz.token_set_ratio(new_pip_name, new_name) + b * fuzz.token_sort_ratio(new_pip_name, new_name) +
    c * fuzz.ratio(new_pip_name, new_name) + d * fuzz.partial_ratio(new_pip_name, new_name)) / (a + b + c + d)


# super_args form is (()...())
def super_func(func, super_args):
  result_sum = 0.0
  for el in super_args:
    result_sum += func(*el)
  return result_sum


def mult_args(super_args, n, x):
  for idx in xrange(len(super_args)):
    super_args[idx] = tuple(super_args[idx][:n]) + tuple([super_args[idx][n] * x]) + tuple(super_args[idx][n+1:])


def div_args(super_args, n, x):
  for idx in xrange(len(super_args)):
    super_args[idx] = tuple(super_args[idx][:n]) + tuple([super_args[idx][n] / x]) + tuple(super_args[idx][n+1:])


# start_arg and stop_args it's like we have function func(z1, z2, x1, x2, x3),
# and z1, z2 - not approximated args, and x1..x3 we have to approximate
# so start_arg will be 2, and stop_arg will be 4 here
def my_least_square(func, right_args, wrong_args, start_arg, stop_arg):
  new_right_args = list(right_args)
  old_right_args = list(right_args)
  for narg in xrange(start_arg, stop_arg + 1):
    diff_with_wrong = super_func(fuzzy_search_func, new_right_args) - super_func(fuzzy_search_func, wrong_args)
    diff_with_old = 99.0
    while (diff_with_old > 1.0 and
      super_func(fuzzy_search_func, new_right_args) - super_func(fuzzy_search_func, wrong_args) >= diff_with_wrong):

      diff_with_wrong = super_func(fuzzy_search_func, new_right_args) - super_func(fuzzy_search_func, wrong_args)
      mult_args(new_right_args, narg, 2.0)
      if super_func(fuzzy_search_func, new_right_args) < super_func(fuzzy_search_func, old_right_args):
        div_args(new_right_args, narg, 4.0)

      diff_with_old = super_func(fuzzy_search_func, new_right_args) - super_func(fuzzy_search_func, old_right_args)
      old_right_args = list(new_right_args)
  return new_right_args


def main():
  pdb.set_trace()
  right_args = []
  wrong_args = []
  right_args_file = open(sys.argv[1])
  for line in right_args_file:
    splitted = re.sub("\s", "", line).split(",")
    right_args.append(tuple(splitted[:2]) + tuple(map(float, splitted[2:])))
  right_args_file.close()

  wrong_args_file = open(sys.argv[2])
  for line in wrong_args_file:
    splitted = re.sub("\s", "", line).split(",")
    wrong_args.append(tuple(splitted[:2]) + tuple(map(float, splitted[2:])))
  wrong_args_file.close()

  print my_least_square(fuzzy_search_func, right_args, wrong_args, 2, 5)


if __name__ == '__main__':
  main()