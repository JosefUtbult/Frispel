# Frispel

## Utveckling

För utveckling kan du köra `web` dockern på din egna dator.

Se till att du har `docker` och `docker-compose` installerat på maskinen.

Kör sedan dockercontainern `web` med docker-compose. **Kör inte alla containrar, då `nginx` containern kommer försöka skapa ett certificat**.

```bash
docker-compose up -d web
```

När du gjort dina ändringar kan du bygga om containern och köra den igen.

```bash
docker-compose down
docker-compose build
docker-compose up -d web
```

## Setup

Fixa en virtuell maskin. På [Vultr](https://www.vultr.com/) kan du skapa en VPS. Använd sedan Cloudflare för att peka URLn till den virtuella maskinens IP.

### Cloudflare

På Cloudflare bör det redan finnas en del konfigurerat för `frispel.rocks`. Gå in på `DNS > Records` och se till att följande records finns.

- Type: `A`, Name `*`, IPv4 address: `VMens IPv4 address`
- Type: `A`, Name `frispel.rocks`, IPv4 address: `VMens IPv4 address`
- Type: `A`, Name `www`, IPv4 address: `VMens IPv4 address`
- Type: `AAAA`, Name `frispel.rocks`, IPv6 address: `VMens IPv6 address` (Tror inte det ska vara nödvändigt)

### VM

Se till att `docker` och `docker-compose` finns på maskinen.

På den virtuella maskinen, generera ssh nycklar och lägg till dem på GitHub.

Klona sedan ner projektet i `/root/Frispel`.

```bash
cd /root
git clone git@github.com:JosefUtbult/Frispel.git
cd Frispel
```

Kopiera över följande filer manuellt med `scp`.

- `frispel-docker/database`
- `frispel-docer/secrets`

Filerna ska finnas på Frispels-driven.

Testa att köra allting manuellt.

```bash
docker-compose up
```

Den bör bygga de två dockercontainerna och köra dem.

Testa om sidan ligger uppe på VMens IP address och på [frispel.rocks](https://www.frispel.rocks).

Du kan avsluta docker-compose med `Ctrl + c`.

### Service

Kopiera över servicefilen till systemd

```bash
cp docker-compose.service /etc/systemd/system/docker-compose.service
```

Starta och enabla servicen

```bash
 systemctl enable docker-compose.service
 systemctl start docker-compose.service
 systemctl status docker-compose.service
```
