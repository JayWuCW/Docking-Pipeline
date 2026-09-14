Due to Vina outputting separate logs for each ligand, the first step involved grouping the fifty
individual outputs into a single dataframe. Once done, I could arrange the ligands by their affinity
for the docking site, allowing for comparison between both groups and individuals within groups. I
then summarised groups by their best scores and mean scores, before plotting the results in two
different histograms. 


logs <- list.files("output/logs", pattern = "_log\\.txt$", full.names = TRUE)

read_score <- function(f) {
  txt <- readLines(f, warn = FALSE)
  rows <- str_match(str_trim(txt), "^(\\d+)\\s+(-?[0-9.]+)\\s+(-?[0-9.]+)\\s+(-?[0-9.]+)$")
  aff  <- as.numeric(rows[!is.na(rows[, 1]), 3])
  tibble(
    ligand  = str_remove(basename(f), "_log\\.txt$"),
    best    = min(aff),
    n_poses = length(aff)
  )
}

results <- map_dfr(logs, read_score) |>
  arrange(best) |>
  mutate(rank = row_number())

write_xlsx(results, "docking_results.csv")

df <- read_csv("docking_results.csv")

df |>
+     arrange(best_affinity_kcal_mol)

df |>
+     arrange(best_affinity_kcal_mol) |>
+     mutate(rank = row_number()) |>
+     filter(label == "control") |>
+     select(ligand_id, best_affinity_kcal_mol, rank)

 df |>
+     group_by(label) |>
+     summarise(
+         n          = n(),
+         mean_score = mean(best_affinity_kcal_mol),
+         best_score = min(best_affinity_kcal_mol)

> ggplot(df, aes(x = best_affinity_kcal_mol)) +
+     geom_histogram(bins = 15, fill = "blue", colour = "white") +
+     geom_vline(
+         data = filter(df, label == "control"),
+         aes(xintercept = best_affinity_kcal_mol),
+         colour = "red"
+     ) +
+     labs(x = "Binding affinity (kcal/mol)", y = "Number of drugs",
+          title = "Docking scores (red lines = known AChE drugs)") +
+     theme_minimal()
>
> ggsave("Docking_Score_Histogram.png", width = 7, height = 5)

> ggplot(df, aes(x = label, y = best_affinity_kcal_mol, fill = label)) +
+     geom_boxplot(alpha = 0.5) +
+     geom_jitter(width = 0.15) +
+     labs(x = NULL, y = "Binding affinity (kcal/mol)") +
+     theme_minimal() +
+     theme(legend.position = "none")
>
> ggsave("controls_vs_background.png", width = 6, height = 5)
