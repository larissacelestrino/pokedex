-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 18/11/2025 às 14:47
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `pokemon`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `pokemon`
--

CREATE TABLE `pokemon` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `tipo1` varchar(50) NOT NULL,
  `tipo2` varchar(50) DEFAULT NULL,
  `treinador` varchar(100) DEFAULT NULL,
  `foto` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `pokemon`
--

INSERT INTO `pokemon` (`id`, `nome`, `tipo1`, `tipo2`, `treinador`, `foto`) VALUES
(1, 'Charmander', 'Fogo', 'Elétrico', '', ''),
(2, 'Pikachu', 'Fogo', 'Fogo', 'Ash', 'original.jpg'),
(3, 'Felicity', 'Gelo', 'Gelo', '--- Selecione um Treinador ---', 'original.jpg'),
(5, 'Lala', 'Água', 'Grama', 'Larimax', 'original.jpg'),
(6, 'Miau', 'Elétrico', 'Lutador', 'Jessica', 'meowth.jpg'),
(8, 'Gengar', 'Fantasma', 'Venenoso', 'Selecione treinador ', 'meowth.jpg');

-- --------------------------------------------------------

--
-- Estrutura para tabela `treinadores`
--

CREATE TABLE `treinadores` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `cidade` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `treinadores`
--

INSERT INTO `treinadores` (`id`, `nome`, `cidade`) VALUES
(1, 'Ash', 'Itatiba'),
(2, 'Larimax', 'Itatiba'),
(3, 'Jessica', 'Itatiba'),
(4, 'Prieto kardashian', 'Belem');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `pokemon`
--
ALTER TABLE `pokemon`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Índices de tabela `treinadores`
--
ALTER TABLE `treinadores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `pokemon`
--
ALTER TABLE `pokemon`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `treinadores`
--
ALTER TABLE `treinadores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
