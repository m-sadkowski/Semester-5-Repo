package lab.aui.app;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Setter
@Getter
@Builder
class Player implements Comparable<Player>, Serializable {
    private final UUID id;
    private final String name;
    private final int number;
    private final Club club;

    static void create(String name, int number, Club club) {
        Player newPlayer = Player.builder()
                .id(UUID.randomUUID())
                .name(name)
                .number(number)
                .club(club)
                .build();

        List<Player> newPlayers = new ArrayList<>(club.getPlayers());
        newPlayers.add(newPlayer);
        club.setPlayers(newPlayers);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, number);
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Player p)) { return false; }
        return this.id.equals(p.id);
    }

    @Override
    public int compareTo(Player other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return name + " (" + number + ")";
    }
}
