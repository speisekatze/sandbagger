# Sandbagger

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Thomas-Walter_sandbagger&metric=alert_status)](https://sonarcloud.io/dashboard?id=Thomas-Walter_sandbagger)[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Thomas-Walter_sandbagger&metric=coverage)](https://sonarcloud.io/dashboard?id=Thomas-Walter_sandbagger)[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=Thomas-Walter_sandbagger&metric=ncloc)](https://sonarcloud.io/dashboard?id=Thomas-Walter_sandbagger)![Sandbagger Docker Image](https://github.com/speisekatze/sandbagger/workflows/Sandbagger%20Docker%20Image/badge.svg?branch=master)

**sandbagger - Aggregates Blocklists from different sources into categories**

This app spawns a simple HTTP(S) server on a given port.
It serves DNSBL-files in multiple categories to feed pfBlockerNG or piHole.
The server removes duplicate hosts from different sources for each category.
The categories and sources are fully customizable.  

---

## Install

You can either pull the image from [dockerhub](https://hub.docker.com/r/speisekatze/sandbagger), creating the image with the Dockerfile
or deploy it with docker-compose.

### Using the image

The configuration is the same for the own created image or the one from dockerhub.
Start the container with the default configuration:

```bash
docker run -d --name sandbagger -p 8080:8080 sandbagger
```

The default config uses a self signed certificate, you can change this by passing some empty environment variables.

```bash
docker run -d --name sandbagger -p 8080:8080 -e CERT= -e KEY= sandbagger
```

If you want to use an own collection of blocklist you have to create a directory which maps into the container. In this directory
create a new file named _blacklists.conf_, see file in ./config for an example.

```bash
docker run -d --name sandbagger -p 8080:8080 -e CERT -e KEY -v /data/volumes/sandbagger:/sandbagger/ext sandbagger
```

You can also provide an own certificate and keyfile in that directory and set the environment variables to the filenames.

## Sources used

I'm using various sources for this project.
At first, I used blocklists of Stephen Black's ["hosts" project](https://github.com/StevenBlack/hosts/) as initial lists.
But decided to take his sources and scrape his update-files for more granular blocklists and his *extensions* as category names.  
Here is a list of all sources currently used in the sandbagger configuration. Feel free to add your sources of blocklists.  

Name: Tiuxo hostlist - social -
Home: <https://github.com/tiuxo/hosts>  
Name: Sinfonietta's social media blocking hosts file -
Home: <https://github.com/Sinfonietta/hostfiles>  
Name: Fake News -
Home: <https://github.com/marktron/fakenews>  
Name: Sinfonietta's gambling blocking hosts file -
Home: <https://github.com/Sinfonietta/hostfiles>  
Name: pornhosts -- a consolidated anti porn hosts file -
Home: <https://github.com/Clefspeare13/pornhosts>  
Name: Sinfonietta's snuff-site blocking hosts file -
Home: <https://github.com/Sinfonietta/hostfiles>  
Name: Tiuxo hostlist - pornography -
Home: <https://github.com/tiuxo/hosts>  
Name: Sinfonietta's porn blocking hosts file -
Home: <https://github.com/Sinfonietta/hostfiles>  
Name: hostsVN -
Home: <https://github.com/bigdargon/hostsVN>  
Name: Mitchell Krog's - Badd Boyz Hosts -
Home: <https://github.com/mitchellkrogza/Badd-Boyz-Hosts>
Name: MVPS hosts file -
Home: <https://winhelp2002.mvps.org/>
Name: Dan Pollock – someonewhocares -
Home: <https://someonewhocares.org/hosts/>
Name: add.2o7Net -
Home: <https://github.com/FadeMind/hosts.extras>
Name: yoyo.org -
Home: <https://pgl.yoyo.org/adservers/>
Name: UncheckyAds -
Home: <https://github.com/FadeMind/hosts.extras>
Name: Steven Black's ad-hoc list -
Home: <https://github.com/StevenBlack/hosts/blob/master/data/StevenBlack/hosts>
Name: KADhosts -
Home: <https://kadantiscam.netlify.com>
Name: add.Spam -
Home: <https://github.com/FadeMind/hosts.extras>
Name: Tiuxo hostlist - ads -
Home: <https://github.com/tiuxo/hosts>
Name: Malware Domain List -
Home: <https://www.malwaredomainlist.com>
Name: AdAway -
Home: <https://adaway.org/>
Name: add.Risk -
Home: <https://github.com/FadeMind/hosts.extras>
Name: add.Dead -
Home: <https://github.com/FadeMind/hosts.extras>

---

---
