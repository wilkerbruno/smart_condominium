-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 02/04/2024 às 03:22
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `smart_condominium`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `areacomum`
--

CREATE TABLE `areacomum` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `descricao` varchar(255) NOT NULL,
  `regras_uso` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `comunicacao`
--

CREATE TABLE `comunicacao` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `titulo` varchar(255) NOT NULL,
  `conteudo` text NOT NULL,
  `data_envio` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `condominio`
--

CREATE TABLE `condominio` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `numero` varchar(10) NOT NULL,
  `endereco` varchar(255) NOT NULL,
  `cidade` varchar(100) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `cep` varchar(20) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `celular` varchar(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `sindico_nome` varchar(100) DEFAULT NULL,
  `sindico_telefone` varchar(20) DEFAULT NULL,
  `sindico_email` varchar(100) DEFAULT NULL,
  `regras_regulamentos` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `condominio`
--

INSERT INTO `condominio` (`id`, `nome`, `numero`, `endereco`, `cidade`, `estado`, `cep`, `telefone`, `celular`, `email`, `sindico_nome`, `sindico_telefone`, `sindico_email`, `regras_regulamentos`) VALUES
(1, 'Residencial Primavera', '', 'Rua das Flores, 100', 'São Paulo', 'SP', '01234-567', '(11) 1234-5678', '(11) 9876-5432', 'contato@residencialprimavera.com', 'Carlos Silva', '(11) 7654-3210', 'carlos.silva@email.com', 'Regras e regulamentos do condomínio Residencial Primavera...'),
(2, 'Parque das Flores', '', 'Av. dos Girassóis, 200', 'Rio de Janeiro', 'RJ', '20000-123', '(21) 5555-5555', '(21) 9876-5432', 'contato@parquedasflores.com', 'Ana Santos', '(21) 8765-4321', 'ana.santos@email.com', 'Regras e regulamentos do condomínio Parque das Flores...'),
(3, 'Vista Bela', '', 'Rua das Palmeiras, 300', 'Belo Horizonte', 'MG', '30000-456', '(31) 3333-3333', '(31) 8765-4321', 'contato@vistabela.com', 'João Oliveira', '(31) 7654-3210', 'joao.oliveira@email.com', 'Regras e regulamentos do condomínio Vista Bela...'),
(4, 'Sol Nascente', '', 'Av. do Sol, 400', 'Brasília', 'DF', '70000-789', '(61) 7777-7777', '(61) 9876-5432', 'contato@solascente.com', 'Maria Silva', '(61) 8765-4321', 'maria.silva@email.com', 'Regras e regulamentos do condomínio Sol Nascente...'),
(5, 'Jardim das Flores', '', 'Alameda das Tulipas, 500', 'Curitiba', 'PR', '80000-901', '(41) 8888-8888', '(41) 9876-5432', 'contato@jardimdasflores.com', 'Pedro Oliveira', '(41) 8765-4321', 'pedro.oliveira@email.com', 'Regras e regulamentos do condomínio Jardim das Flores...');

-- --------------------------------------------------------

--
-- Estrutura para tabela `documentolegal`
--

CREATE TABLE `documentolegal` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `tipo_documento` varchar(50) NOT NULL,
  `descricao` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `financeiro`
--

CREATE TABLE `financeiro` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `tipo_transacao` varchar(20) NOT NULL,
  `descricao_transacao` varchar(255) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `data_transacao` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `funcionario`
--

CREATE TABLE `funcionario` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `nome` varchar(100) NOT NULL,
  `cargo` varchar(50) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `horario_trabalho` varchar(100) DEFAULT NULL,
  `salario_funcionario` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `funcionario`
--

INSERT INTO `funcionario` (`id`, `condominio_id`, `nome`, `cargo`, `telefone`, `email`, `horario_trabalho`, `salario_funcionario`) VALUES
(1, 1, 'Maria Santos', 'sindico', '(11) 1111-1111', 'maria.santos@residencialprimavera.com', 'Segunda a sexta, 08:00 - 17:00', 2500),
(2, 5, 'José Silva', 'sindico', '(11) 2222-2222', 'jose.silva@residencialprimavera.com', 'Segunda a sexta, 08:00 - 17:00', 3000),
(3, 2, 'Ana Oliveira', 'sindico', '(21) 3333-3333', 'ana.oliveira@parquedasflores.com', 'Segunda a sexta, 07:00 - 16:00', 2400),
(4, 3, 'Paulo Souza', 'sindico', '(31) 4444-4444', 'paulo.souza@vistabela.com', 'Segunda a sexta, 09:00 - 18:00', 2800),
(5, 4, 'Luciana Costa', 'sindico', '(61) 5555-5555', 'luciana.costa@solascente.com', 'Segunda a sexta, 08:30 - 17:30', 2600);

-- --------------------------------------------------------

--
-- Estrutura para tabela `manutencaoservicos`
--

CREATE TABLE `manutencaoservicos` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `descricao_servico` text NOT NULL,
  `data_servico` date NOT NULL,
  `custo` decimal(10,2) DEFAULT NULL,
  `prestador_servico` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `morador`
--

CREATE TABLE `morador` (
  `id` int(11) NOT NULL,
  `unidade_id` int(11) DEFAULT NULL,
  `nome` varchar(100) NOT NULL,
  `data_nascimento` date DEFAULT NULL,
  `documento_identidade` varchar(20) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `relacao_unidade` varchar(50) NOT NULL,
  `veiculo_placa` varchar(20) DEFAULT NULL,
  `veiculo_modelo` varchar(50) DEFAULT NULL,
  `veiculo_cor` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `morador`
--

INSERT INTO `morador` (`id`, `unidade_id`, `nome`, `data_nascimento`, `documento_identidade`, `telefone`, `email`, `relacao_unidade`, `veiculo_placa`, `veiculo_modelo`, `veiculo_cor`) VALUES
(1, 1, 'Ana Oliveira', '1985-03-15', '123456789', '(11) 9999-8888', 'ana.oliveira@email.com', 'Proprietário', 'ABC-1234', 'Toyota Corolla', 'Prata'),
(2, 1, 'Pedro Oliveira', '1978-07-22', '987654321', '(11) 8888-7777', 'pedro.oliveira@email.com', 'Inquilino', 'XYZ-9876', 'Honda Civic', 'Preto'),
(3, 2, 'Lucas Santos', '1990-10-05', '456789123', '(11) 7777-6666', 'lucas.santos@email.com', 'Proprietário', 'DEF-5678', 'Volkswagen Golf', 'Azul'),
(4, 3, 'Marina Costa', '1982-05-20', '654321987', '(11) 6666-5555', 'marina.costa@email.com', 'Proprietário', 'GHI-3456', 'Ford Fiesta', 'Vermelho'),
(5, 3, 'Fernanda Silva', '1995-12-12', '789123456', '(11) 5555-4444', 'fernanda.silva@email.com', 'Inquilino', 'JKL-9012', 'Chevrolet Onix', 'Branco'),
(6, 6, 'Gustavo Oliveira', '1987-08-18', '987654321', '(21) 9999-8888', 'gustavo.oliveira@email.com', 'Proprietário', 'MNO-2345', 'Fiat Uno', 'Vermelho'),
(7, 6, 'Amanda Santos', '1993-04-25', '456789123', '(21) 8888-7777', 'amanda.santos@email.com', 'Inquilino', 'PQR-6789', 'Renault Sandero', 'Prata'),
(8, 7, 'Juliana Costa', '1975-11-30', '654321987', '(21) 7777-6666', 'juliana.costa@email.com', 'Proprietário', 'STU-7890', 'Chevrolet Prisma', 'Preto'),
(9, 8, 'Rafael Silva', '1988-06-08', '789123456', '(21) 6666-5555', 'rafael.silva@email.com', 'Proprietário', 'VWX-1234', 'Hyundai HB20', 'Azul'),
(10, 8, 'Camila Oliveira', '1980-03-10', '321987654', '(21) 5555-4444', 'camila.oliveira@email.com', 'Inquilino', 'YZA-5678', 'Volkswagen Polo', 'Branco'),
(11, 9, 'Fábio Santos', '1984-09-03', '987654321', '(31) 9999-8888', 'fabio.santos@email.com', 'Proprietário', 'BCD-3456', 'Toyota Etios', 'Prata'),
(12, 9, 'Laura Costa', '1979-02-28', '456789123', '(31) 8888-7777', 'laura.costa@email.com', 'Proprietário', 'EFG-6789', 'Fiat Palio', 'Vermelho'),
(13, 10, 'Gabriel Silva', '1992-07-14', '654321987', '(31) 7777-6666', 'gabriel.silva@email.com', 'Inquilino', 'HIJ-7890', 'Renault Duster', 'Preto'),
(14, 11, 'Carolina Oliveira', '1986-12-22', '789123456', '(31) 6666-5555', 'carolina.oliveira@email.com', 'Proprietário', 'KLM-1234', 'Honda Fit', 'Azul'),
(15, 11, 'Matheus Santos', '1981-05-17', '321987654', '(31) 5555-4444', 'matheus.santos@email.com', 'Inquilino', 'NOP-5678', 'Chevrolet Spin', 'Branco'),
(16, 12, 'Vanessa Costa', '1989-11-11', '987654321', '(61) 9999-8888', 'vanessa.costa@email.com', 'Proprietário', 'PQR-3456', 'Fiat Toro', 'Prata'),
(17, 12, 'Bruno Silva', '1977-06-04', '456789123', '(61) 8888-7777', 'bruno.silva@email.com', 'Inquilino', 'STU-6789', 'Volkswagen Voyage', 'Vermelho'),
(18, 13, 'Fernando Oliveira', '1980-03-29', '654321987', '(61) 7777-6666', 'fernando.oliveira@email.com', 'Proprietário', 'VWX-7890', 'Chevrolet Tracker', 'Preto'),
(19, 14, 'Aline Santos', '1991-08-15', '789123456', '(61) 6666-5555', 'aline.santos@email.com', 'Proprietário', 'YZA-1234', 'Ford Ecosport', 'Azul'),
(20, 14, 'Daniel Costa', '1976-12-08', '321987654', '(61) 5555-4444', 'daniel.costa@email.com', 'Inquilino', 'BCD-5678', 'Toyota Hilux', 'Branco'),
(21, 15, 'Isabela Oliveira', '1994-04-20', '987654321', '(41) 9999-8888', 'isabela.oliveira@email.com', 'Proprietário', 'EFG-3456', 'Renault Kwid', 'Prata'),
(22, 15, 'Gustavo Santos', '1983-09-16', '456789123', '(41) 8888-7777', 'gustavo.santos@email.com', 'Inquilino', 'HIJ-6789', 'Fiat Siena', 'Vermelho'),
(23, 16, 'Julia Silva', '1988-02-09', '654321987', '(41) 7777-6666', 'julia.silva@email.com', 'Proprietário', 'KLM-7890', 'Chevrolet', 'Vermelho');

-- --------------------------------------------------------

--
-- Estrutura para tabela `seguranca`
--

CREATE TABLE `seguranca` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `tipo_registro` varchar(50) NOT NULL,
  `descricao` text NOT NULL,
  `data_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `unidade`
--

CREATE TABLE `unidade` (
  `id` int(11) NOT NULL,
  `condominio_id` int(11) DEFAULT NULL,
  `numero_unidade` varchar(20) NOT NULL,
  `proprietario_residente` varchar(100) NOT NULL,
  `telefone_proprietario` varchar(20) DEFAULT NULL,
  `email_proprietario` varchar(100) DEFAULT NULL,
  `tipo_unidade` varchar(50) NOT NULL,
  `status` varchar(20) NOT NULL,
  `area` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `unidade`
--

INSERT INTO `unidade` (`id`, `condominio_id`, `numero_unidade`, `proprietario_residente`, `telefone_proprietario`, `email_proprietario`, `tipo_unidade`, `status`, `area`) VALUES
(1, 1, '101', 'Carlos Silva', '(11) 1234-5678', 'carlos.silva@email.com', 'Apartamento', 'Ocupada', 100.00),
(2, 1, '102', 'Mariana Santos', '(11) 2345-6789', 'mariana.santos@email.com', 'Apartamento', 'Disponível', 90.00),
(3, 1, '201', 'João Oliveira', '(11) 3456-7890', 'joao.oliveira@email.com', 'Cobertura', 'Alugado', 150.00),
(4, 1, '202', 'Ana Costa', '(11) 4567-8901', 'ana.costa@email.com', 'Apartamento', 'Disponível', 95.00),
(5, 1, '301', 'Paulo Souza', '(11) 5678-9012', 'paulo.souza@email.com', 'Apartamento', 'Ocupada', 110.00),
(6, 2, 'A1', 'Pedro Oliveira', '(21) 5555-5555', 'pedro.oliveira@email.com', 'Casa', 'Ocupada', 200.00),
(7, 2, 'A2', 'Luciana Costa', '(21) 6666-6666', 'luciana.costa@email.com', 'Apartamento', 'Disponível', 85.00),
(8, 2, 'B1', 'Ana Oliveira', '(21) 7777-7777', 'ana.oliveira@email.com', 'Cobertura', 'Ocupada', 160.00),
(9, 2, 'B2', 'Fernando Silva', '(21) 8888-8888', 'fernando.silva@email.com', 'Apartamento', 'Disponível', 100.00),
(10, 2, 'C1', 'Marta Santos', '(21) 9999-9999', 'marta.santos@email.com', 'Apartamento', 'Ocupada', 120.00),
(11, 3, '101', 'Carla Oliveira', '(31) 1111-1111', 'carla.oliveira@email.com', 'Apartamento', 'Ocupada', 95.00),
(12, 3, '102', 'Renato Silva', '(31) 2222-2222', 'renato.silva@email.com', 'Cobertura', 'Disponível', 140.00),
(13, 3, '201', 'Mariana Costa', '(31) 3333-3333', 'mariana.costa@email.com', 'Apartamento', 'Alugado', 105.00),
(14, 3, '202', 'Joana Santos', '(31) 4444-4444', 'joana.santos@email.com', 'Apartamento', 'Disponível', 100.00),
(15, 3, '301', 'Luiz Oliveira', '(31) 5555-5555', 'luiz.oliveira@email.com', 'Casa', 'Ocupada', 180.00),
(16, 4, '101', 'Ricardo Santos', '(61) 1111-1111', 'ricardo.santos@email.com', 'Apartamento', 'Disponível', 90.00),
(17, 4, '102', 'Carolina Oliveira', '(61) 2222-2222', 'carolina.oliveira@email.com', 'Apartamento', 'Ocupada', 100.00),
(18, 4, '201', 'Roberto Silva', '(61) 3333-3333', 'roberto.silva@email.com', 'Casa', 'Alugado', 150.00),
(19, 4, '202', 'Fernanda Costa', '(61) 4444-4444', 'fernanda.costa@email.com', 'Apartamento', 'Ocupada', 110.00),
(20, 4, '301', 'Paula Santos', '(61) 5555-5555', 'paula.santos@email.com', 'Cobertura', 'Disponível', 160.00),
(21, 5, '101', 'Guilherme Oliveira', '(41) 1111-1111', 'guilherme.oliveira@email.com', 'Apartamento', 'Ocupada', 100.00),
(22, 5, '102', 'Helena Silva', '(41) 2222-2222', 'helena.silva@email.com', 'Cobertura', 'Alugado', 150.00),
(23, 5, '201', 'Luis Costa', '(41) 3333-3333', 'luis.costa@email.com', 'Casa', 'Alugado', 180.00),
(24, 5, '202', 'Alice Santos', '(41) 4444-4444', 'alice.santos@email.com', 'Apartamento', 'Disponível', 95.00),
(25, 5, '301', 'Júlia Oliveira', '(41) 5555-5555', 'julia.oliveira@email.com', 'Apartamento', 'Ocupada', 110.00);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `areacomum`
--
ALTER TABLE `areacomum`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `comunicacao`
--
ALTER TABLE `comunicacao`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `condominio`
--
ALTER TABLE `condominio`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `documentolegal`
--
ALTER TABLE `documentolegal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `financeiro`
--
ALTER TABLE `financeiro`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `funcionario`
--
ALTER TABLE `funcionario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `manutencaoservicos`
--
ALTER TABLE `manutencaoservicos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `morador`
--
ALTER TABLE `morador`
  ADD PRIMARY KEY (`id`),
  ADD KEY `unidade_id` (`unidade_id`);

--
-- Índices de tabela `seguranca`
--
ALTER TABLE `seguranca`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- Índices de tabela `unidade`
--
ALTER TABLE `unidade`
  ADD PRIMARY KEY (`id`),
  ADD KEY `condominio_id` (`condominio_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `areacomum`
--
ALTER TABLE `areacomum`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `comunicacao`
--
ALTER TABLE `comunicacao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `condominio`
--
ALTER TABLE `condominio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `documentolegal`
--
ALTER TABLE `documentolegal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `financeiro`
--
ALTER TABLE `financeiro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `funcionario`
--
ALTER TABLE `funcionario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `manutencaoservicos`
--
ALTER TABLE `manutencaoservicos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `morador`
--
ALTER TABLE `morador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de tabela `seguranca`
--
ALTER TABLE `seguranca`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `unidade`
--
ALTER TABLE `unidade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `areacomum`
--
ALTER TABLE `areacomum`
  ADD CONSTRAINT `areacomum_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `comunicacao`
--
ALTER TABLE `comunicacao`
  ADD CONSTRAINT `comunicacao_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `documentolegal`
--
ALTER TABLE `documentolegal`
  ADD CONSTRAINT `documentolegal_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `financeiro`
--
ALTER TABLE `financeiro`
  ADD CONSTRAINT `financeiro_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `funcionario`
--
ALTER TABLE `funcionario`
  ADD CONSTRAINT `funcionario_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `manutencaoservicos`
--
ALTER TABLE `manutencaoservicos`
  ADD CONSTRAINT `manutencaoservicos_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `morador`
--
ALTER TABLE `morador`
  ADD CONSTRAINT `morador_ibfk_1` FOREIGN KEY (`unidade_id`) REFERENCES `unidade` (`id`);

--
-- Restrições para tabelas `seguranca`
--
ALTER TABLE `seguranca`
  ADD CONSTRAINT `seguranca_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);

--
-- Restrições para tabelas `unidade`
--
ALTER TABLE `unidade`
  ADD CONSTRAINT `unidade_ibfk_1` FOREIGN KEY (`condominio_id`) REFERENCES `condominio` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
