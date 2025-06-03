#!/bin/bash
curl -L -o ./used_cars.zip \
  https://www.kaggle.com/api/v1/datasets/download/ananaymital/us-used-cars-dataset

unzip used_cars.zip