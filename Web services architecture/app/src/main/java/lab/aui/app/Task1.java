package lab.aui.app;

import java.io.*;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ForkJoinPool;
import java.util.stream.Collectors;

class Task1 {
    static void execute() {
        List<Club> clubs = createTestData();
        Set<Player> players = getUniquePlayers(clubs);

        featureFirstAndSecond(clubs);
        featureThird(players);
        featureFourth(players);
        featureFifth(players);
        featureSixth(clubs);
        featureSeventh(clubs);
    }

    private static List<Club> createTestData() {
        Club fcb = Club.create("FC Barcelona", "Camp Nou");
        Player.create("Robert Lewandowski", 9, fcb);
        Player.create("Lamine Yamal", 10, fcb);
        Player.create("Pedri", 8, fcb);

        Club rm = Club.create("Real Madrid", "Bernabeu");
        Player.create("Kylian Mbappe", 10, rm);
        Player.create("Arda Guler", 15, rm);
        Player.create("Dani Carvajal", 2, rm);

        return List.of(fcb, rm);
    }

    private static Set<Player> getUniquePlayers(List<Club> clubs) {
        return clubs.stream()
                .flatMap(club -> club.getPlayers().stream())
                .collect(Collectors.toSet());
    }

    private static void featureFirstAndSecond(List<Club> clubs) {
        System.out.println("\nFeatures 1 & 2: ");
        clubs.forEach(System.out::println);
    }

    private static void featureThird(Set<Player> playersSet) {
        System.out.println("\nFeature 3: ");
        playersSet.forEach(System.out::println);
    }

    private static void featureFourth(Set<Player> playersSet) {
        System.out.println("\nFeature 4: ");
        playersSet.stream()
                .filter(player -> player.getNumber() <= 10)
                .sorted(Comparator.comparing(Player::getName))
                .forEach(System.out::println);
    }

    private static void featureFifth(Set<Player> playersSet) {
        System.out.println("\nFeature 5: ");
        List<PlayerDto> playersDto = playersSet.stream()
                .map(PlayerMapper::toDto)
                .sorted()
                .toList();
        playersDto.forEach(System.out::println);
    }

    private static void featureSixth(List<Club> clubs) {
        System.out.println("\nFeature 6: ");
        try (FileOutputStream fileOut = new FileOutputStream("clubs.ser");
             ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
            out.writeObject(clubs);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        try (FileInputStream fileIn = new FileInputStream("clubs.ser");
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            List<Club> newClubs = (List<Club>) in.readObject();
            newClubs.forEach(System.out::println);
        } catch (IOException | ClassNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void featureSeventh(List<Club> clubs) {
        System.out.println("\nFeature 7: ");
        try (ForkJoinPool customPool = new ForkJoinPool(2)) {
            customPool.submit(() ->
                    clubs.parallelStream().forEach(club -> {
                        System.out.println(Thread.currentThread().getName()
                                + " is processing " + club.getName());
                        club.getPlayers().forEach(player -> {
                            System.out.println(player);
                            try {
                                Thread.sleep(3000);
                            } catch (InterruptedException e) {
                                System.out.println(e.getMessage());
                            }
                        });
                    })
            ).get();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
