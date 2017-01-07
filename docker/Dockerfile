FROM ubuntu:16.04
MAINTAINER Koki Takahashi <hakatasiloving@gmail.com>

RUN apt-get -y update
RUN apt-get install -y texlive-lang-cjk texlive-fonts-recommended texlive-latex-extra texlive-fonts-extra texlive-lang-greek texlive-generic-recommended texlive-math-extra texlive-science potrace imagemagick build-essential --no-install-recommends
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/sbin/init"]
