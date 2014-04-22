From vorstand-bounces@stratum0.org  Mon Apr 21 23:32:23 2014
Return-Path: <vorstand-bounces@stratum0.org>
X-Original-To: valodim@mugenguild.com
Delivered-To: valodim@mugenguild.com
Received: from stratum0.org (mail.nerdpapi.de [178.32.53.3])
	by mail.mugenguild.com (Postfix) with ESMTPS id 601C3AC0C0
	for <valodim@mugenguild.com>; Mon, 21 Apr 2014 23:32:23 +0200 (CEST)
Received: from [192.168.1.106] (localhost.localdomain [127.0.0.1])
	by stratum0.org (Postfix) with ESMTP id 20BCE2301CA9;
	Mon, 21 Apr 2014 21:32:22 +0000 (UTC)
X-Original-To: vorstand@stratum0.org
Delivered-To: vorstand@stratum0.org
Received: from mail.mugenguild.com (mail.mugenguild.com [78.47.123.84])
	(using TLSv1 with cipher ADH-AES256-SHA (256/256 bits))
	(No client certificate requested)
	by stratum0.org (Postfix) with ESMTPS id 0989C230013A
	for <vorstand@stratum0.org>; Mon, 21 Apr 2014 21:32:19 +0000 (UTC)
Received: by mail.mugenguild.com (Postfix, from userid 1000)
	id 88010AC0C0; Mon, 21 Apr 2014 23:32:19 +0200 (CEST)
Date: Mon, 21 Apr 2014 23:32:19 +0200
From: Valodim Skywalker <valodim@mugenguild.com>
To: Vorstandsverteiler <vorstand@stratum0.org>
Message-ID: <20140421213219.GA15761@mugenguild.com>
Mail-Followup-To: Vorstandsverteiler <vorstand@stratum0.org>
MIME-Version: 1.0
User-Agent: Mutt/1.5.22.1-rc1 (2013-10-16)
Subject: [#StratumV] [antrag] testantrag
X-BeenThere: vorstand@stratum0.org
X-Mailman-Version: 2.1.13
Precedence: list
List-Id: "Vorstand des Stratum 0 e.V." <vorstand.stratum0.org>
List-Unsubscribe: <http://lists.stratum0.org/mailman/options/vorstand>,
	<mailto:vorstand-request@stratum0.org?subject=unsubscribe>
List-Archive: <http://lists.stratum0.org/mailman/private/vorstand>
List-Post: <mailto:vorstand@stratum0.org>
List-Help: <mailto:vorstand-request@stratum0.org?subject=help>
List-Subscribe: <http://lists.stratum0.org/mailman/listinfo/vorstand>,
	<mailto:vorstand-request@stratum0.org?subject=subscribe>
Content-Type: multipart/mixed; boundary="===============1114394660=="
Sender: vorstand-bounces@stratum0.org
Errors-To: vorstand-bounces@stratum0.org


--===============1114394660==
Content-Type: multipart/signed; micalg=pgp-sha1;
	protocol="application/pgp-signature"; boundary="J/dobhs11T7y2rNN"
Content-Disposition: inline


--J/dobhs11T7y2rNN
Content-Type: text/plain; charset=us-ascii
Content-Disposition: inline
Content-Transfer-Encoding: quoted-printable

Hi, bin auf dem Easterhegg endlich mal dazu kommen ein vote tallying
tool zu basteln. Das mail parsen ist soweit fertig denke ich,=20

ich brauche zum testen meines antrags tallying tools mal einen
testantrag.

Momentan wichtig fuer das tool:
- antraege muessen mit [antrag] markiert werden
- In-Reply-To header muss korrekt gesetzt sein. das ist soweit ich das
  ueberblicken kann schon immer ueberall der fall gewesen
- fuer votes muss in der mail +1, -1 oder ~0 in einer einzelnen zeile
  (!) vorkommen

Bitte mal in allen varianten probevoten.

 - V


--J/dobhs11T7y2rNN
Content-Type: application/pgp-signature

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

iQIcBAEBAgAGBQJTVY5jAAoJEHvRgyDerfoRCb8P/0fWIPZ0Qy0X6CPhxV4t+iKE
3ELXnSSXkek6jLAs2RH7Zy7yOPlRd/GuJ7K9X0i2ijqz2so4x6jSUKyD/Xid6rju
oXhiSZbwNQJCNtH9xCY1fmrTFKb/C6MirbuwlK0NoOEJLEfNtgBhu+Cp91+MDXJS
F8YcFZ44ecBzTcnEMnUr5DhdqX9EYn0sZVvwFm9dlc/zJuQGh7dfGAucudF/ljWl
d6YGqvlIHxZOIFNUpVcG0WC54ILlMR2kH4h5rkh2TD3JJvkiipFsTFRGqlPBHp+d
KLc6wbj26LSe0znn7W1/K/A469uS5HGOMW1gWxW/qnlv3nLf5uDsn0+aYdPQlfub
rXNoaq1pdv9tj7d+5dMKguNJRcNP3C7JYzJsBwCSgeFPkJ3KMHyEnxkA3gp6MJQV
VVd2tyqxt80p/EfB5sov1JinvBSRHyFZGRMdP3TvhAROzyzeKM1YmhONk7NJ2onr
0cFCB8TiIvZYIu2Wb/H742uoQgrZ6RwI6W7kwg4Q0ecnBBboHnW5vG1x/lEaqjJm
4XiVSJRhBXBoNjMhogQbtbBMTYT2PKuIunRFN2ar9C4qwu0fINUnvsaA6f0l7zoB
i/r2L9P2at4CyNLnXcfKZsdKDQMtuvmrJn291YtXmjhuTOfcIF9gJmvulUD47fKT
8usuX5XU02vnugtMzFTV
=woLD
-----END PGP SIGNATURE-----

--J/dobhs11T7y2rNN--

--===============1114394660==
Content-Type: text/plain; charset="iso-8859-1"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline

_______________________________________________
vorstand mailing list
vorstand@stratum0.org
http://lists.stratum0.org/mailman/listinfo/vorstand

--===============1114394660==--
