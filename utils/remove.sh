#!/bin/bash

if [ -d "accounts/migrations" ]
then
    cd accounts/migrations
    find . -type f -not -name '__init__.py' -delete
    cd ..
    rm -rf __pycache__

    cd ../ACN
    rm -rf __pycache__
    cd ..
fi

if [ -d "products/migrations" ]
then
    cd events/migrations
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
    cd chats/migrations
    find . -type f -not -name '__init__.py' -delete
    cd ..
    rm -rf __pycache__
    cd ..
fi


