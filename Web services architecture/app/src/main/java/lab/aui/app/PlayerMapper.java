package lab.aui.app;

import lombok.experimental.UtilityClass;

@UtilityClass
class PlayerMapper {
    static PlayerDto toDto(Player player) {
        return PlayerDto.builder()
                .id(player.getId())
                .name(player.getName())
                .number(player.getNumber())
                .clubName(player.getClub().getName())
                .build();
    }
}
