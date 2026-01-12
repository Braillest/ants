FROM mcr.microsoft.com/dotnet/sdk:10.0

WORKDIR /aspnet

RUN apt update
RUN apt upgrade -y

RUN dotnet dev-certs https --trust
RUN dotnet tool install --global dotnet-ef
ENV PATH="$PATH:/root/.dotnet/tools"

# ENTRYPOINT sleep infinity
ENTRYPOINT dotnet run --project Queen.API
