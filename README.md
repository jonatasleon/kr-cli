# Killers Roms CLI
> CLI tool to search and download roms from [Killers Roms][kr-website].

`kr-cli` allows to search and download roms published by [Killers Roms][kr-website] through command line interface.

![Demo usage of kr-cli][demo-gif]

## Installation

```sh
pip install kr-cli
```

## Usage example

### `search` command

Basic usage
```sh
kr search genesis sonic
```

Ordering
```sh
kr search genesis sonic --order-by title --asc
```

Quiet mode shows only the link to rom's webpage
```sh
kr search genesis sonic --quiet # or -q
```

### `download` command

`download` command wait the rom's webpage as argument
```sh
kr download https://roms-download.com/roms/sega-genesis/sonic-knuckles-usa
```

It's possible combine download with `search -q` command
```sh
kr search genesis sonic -q | kr download
```

Defining output directory
```sh
kr search genesis sonic -q | head -n 1 | kr download -d /tmp
```

## Contributing

1. [Fork it][fork-it]
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

[kr-website]: https://roms-download.com/
[demo-gif]: https://raw.githubusercontent.com/jonatasleon/kr-cli/main/demo.gif
[fork-it]: https://github.com/jonatasleon/kr-cli/fork
