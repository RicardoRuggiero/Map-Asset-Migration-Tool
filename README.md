# Map Asset Migration Tool

Este *add-on* para **Blender** permite a importação estruturada e o processamento de mapas e modelos tridimensionais (arquivos `.gnd`, `.rsm` e `.rsw`), lendo os dados brutos de relevo, instâncias e materiais para que possam ser manipulados nativamente no ambiente 3D e, posteriormente, exportados para os formatos OBJ, FBX ou glTF.

<img width="1600" height="857" alt="image" src="https://github.com/user-attachments/assets/9c1c1e80-0c02-47d1-9988-fcd758e54568" />


## Principais Funcionalidades

* **Leitura de Cenário (`.rsw`):** Orquestra a planta do mapa, posicionando instâncias de objetos, construções e propriedades do mundo nas coordenadas globais exatas.
* **Geração de Terreno (`.gnd`):** Reconstrói a malha de relevo contínua, aplicando os mapas de luz, coordenadas UV e texturas dinamicamente.
* **Importação de Modelos Estáticos (`.rsm`):** Lê nós de geometria e aplica os materiais correspondentes, ignorando automaticamente polígonos inválidos ou sobrepostos da malha original.

## Notas Técnicas e Desenvolvimento

Este projeto encontra-se em fase ativa de refatoração e desenvolvimento. Para implementação e uso prático, recomenda-se verificar o estado atual do código-fonte e compatibilidade com a API.

* **Integração de Dados:** A arquitetura do *parser* requer que os diretórios de modelos e texturas operem no mesmo nível hierárquico (caminhos relativos) do orquestrador de cena. Além disso, os arquivos-fonte devem obrigatoriamente preservar sua codificação de caracteres (*encoding*) nativa original para garantir a resolução correta dos *paths* durante o processamento.

* **Ambiente de Depuração:** Para eventuais manutenções ou modificações estruturais neste *add-on*, recomendo a utilização do *VS Code* em conjunto com a extensão *Blender Development* de _Jacques Lucke_.  Essa configuração permite o *hot-reload* automático do código no Blender e o acompanhamento de *stack traces* e *logs* de erro em tempo real.


* Este projeto é livre para uso não comercial e de código aberto sob a licença AGPL v3. Para uso comercial em projetos de código fechado, ferramentas internas ou distribuição como serviço de rede, entre em contato para adquirir uma licença comercial.
---

### Licença e Créditos

*Modificado e atualizado* para o Blender 5.1+ por [Ricardo Ruggiero](https://github.com/RicardoRuggiero). Baseado no trabalho *original* de Colin Basnett sob a licença MIT. 

**Nota sobre o contato com o autor original:** Houve uma tentativa de comunicação com o criador original deste projeto utilizando o único canal disponibilizado publicamente por ele. No entanto, o perfil não aceita solicitações de contato e sua atividade encontra-se restrita/privada na plataforma (*"@cmbasnett's activity is private"*). Em absoluto respeito à sua privacidade e aos limites da comunidade open-source, optou-se por não buscar meios alternativos de contato pela internet, evitando qualquer abordagem invasiva.
