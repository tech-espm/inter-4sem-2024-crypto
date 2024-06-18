import app = require("teem");

class IndexRoute {
	public async index(req: app.Request, res: app.Response) {
		let hoje = new Date();

		let mes = hoje.getMonth() + 1;
		let dia = hoje.getDate();
		let moedas: any[];

		await app.sql.connect(async sql => {
			moedas = await sql.query("SELECT idcurrency, nome FROM currency");
		});

		let opcoes = {
			ano: hoje.getFullYear(),
			mes: (mes < 10 ? "0" + mes : mes),
			dia: (dia < 10 ? "0" + dia : dia),
			moedas: moedas
		};

		res.render("index/index", opcoes);
	}

	public async sobre(req: app.Request, res: app.Response) {
		let opcoes = {
			titulo: "Sobre"
		};

		res.render("index/sobre", opcoes);
	}

	@app.http.post()
	public async obterDados(req: app.Request, res: app.Response) {
		let selecao: number[] = req.body?.selecao || [];
		let dados: any[] = [];

		await app.sql.connect(async sql => {
			for (let i = 0; i < selecao.length; i++) {
				const result = await sql.query(`SELECT * FROM (
    					SELECT 
    					    l.data AS original_data, 
    					    date_format(l.data, '%d/%m/%Y') AS data, 
    					    IFNULL(r.valor, 0) AS valor, 
    					    c.sigla 
    					FROM leitura l
    					INNER JOIN currency c ON c.idcurrency = ?
    					LEFT JOIN ranking r ON r.idleitura = l.idleitura AND r.idcurrency = c.idcurrency
    					ORDER BY l.data DESC
    					LIMIT 10
						) tmp
						ORDER BY tmp.original_data;`, selecao[i]);

				dados.push(result);
			}
		});

		res.json(dados);
	}
}

export = IndexRoute;
