#!/bin/bash

if [ -d "accounts/migrations" ]
then
    cd accounts/migrations
    find . -type f -not -name '__init__.py' -delete
    cd ..
    rm -rf __pycache__

    cd ../crypto
    rm -rf __pycache__
    cd ..
fi

if [ -d "products/migrations" ]
then
    cd products/migrations
    find . -type f -not -name '__init__.py' -delete
    cd ..
    rm -rf __pycache__
    cd ..
fi

if [ -d "home/migrations" ]
then
    cd home/migrations
    find . -type f -not -name '__init__.py' -delete
    cd ..
    rm -rf __pycache__
    cd ..
fi

if [ -d "twits/migrations" ]
then
    cd twits/migrations
    find . -type f -not -name '__init__.py' -delete
    cd ..
    rm -rf __pycache__
    cd ..
fi


