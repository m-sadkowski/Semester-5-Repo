package lab.aui.app;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Setter
@Getter
@Builder
class Club implements Comparable<Club>, Serializable {
    private final UUID id;
    private final String name;
    private final String stadiumName;
    private List<Player> players;

    static Club create(String name, String stadiumName) {
        return Club.builder()
                .id(UUID.randomUUID())
                .name(name)
                .stadiumName(stadiumName)
                .players(List.of())
                .build();
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, stadiumName, players);
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Club c)) { return false; }
        return this.id.equals(c.id);
    }

    @Override
    public int compareTo(Club other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return "Club: " + name + "(stadium: " + stadiumName + ")" + ", players: " + players;
    }
}
