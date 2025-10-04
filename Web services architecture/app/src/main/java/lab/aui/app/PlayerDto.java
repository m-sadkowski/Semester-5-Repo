package lab.aui.app;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
class PlayerDto implements Comparable<PlayerDto> {
    private final UUID id;
    private final String name;
    private final int number;
    private final String clubName;

    @Override
    public int compareTo(PlayerDto other) {
        return this.id.compareTo(other.id);
    }
}
