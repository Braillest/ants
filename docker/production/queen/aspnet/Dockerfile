FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /wrychain
RUN apt update
RUN apt upgrade -y
COPY ./src/backend/ .
RUN dotnet publish -c Release -o /publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /wrychain
COPY --from=build /publish .
ENTRYPOINT dotnet Wrychain.API.dll
