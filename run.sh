#!/bin/bash
docker run -v /Users/bensonlin/Project/CMU/14848_Cloud_Infra/14848_Cloud_Infra_A5:/temp --rm -it -p 8888:8888 -e ACCEPT_EULA=yes mcr.microsoft.com/mmlspark/release
