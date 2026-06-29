FROM mcr.microsoft.com/dotnet/sdk:10.0

WORKDIR /aspnet

RUN apt update
RUN apt upgrade -y

RUN EXIT_CODE=0
RUN dotnet dev-certs https --trust || EXIT_CODE=$?
RUN if [ $EXIT_CODE -ne 0 ] && [ $EXIT_CODE -ne 4 ]; then echo "dotnet dev-certs https --trust failed with exit code $EXIT_CODE"; exit $EXIT_CODE; fi
RUN dotnet tool install --global dotnet-ef
ENV PATH="$PATH:/root/.dotnet/tools"

ENTRYPOINT sleep infinity
# ENTRYPOINT dotnet run --project Queen.API
